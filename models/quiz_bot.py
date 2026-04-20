import json
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class RealEstateQuizBot:
    def __init__(self, properties_file="property_data.json"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        # Using llama3-8b for faster generation to avoid frontend timeouts
        self.llm = ChatGroq(
            groq_api_key=api_key, 
            model="llama-3.3-70b-versatile", 
            temperature=0.7
        )
        
        self.properties = self._load_properties(properties_file)
        self.context = self._build_context()
        self._setup_chains()
        
    def _load_properties(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading properties: {e}")
            return []
    
    def _build_context(self):
        if not self.properties: return ""
        context = "Property Listings:\n"
        for p in self.properties:
            context += f"- {p['title']} ({p['type']}): ${p['price']}. {p['bedrooms']}BR, {p['bathrooms']}BA. {p['description']}\n"
        return context
    
    def _setup_chains(self):
        # Question Generation
        self.q_template = PromptTemplate(
            input_variables=["context", "difficulty"],
            template="""Based on this data: {context}
            Generate one {difficulty} MCQ.
            Format exactly:
            QUESTION: [Question]
            A) [Opt]
            B) [Opt]
            C) [Opt]
            D) [Opt]
            ANSWER: [A, B, C, or D]
            EXPLANATION: [Brief text]"""
        )
        self.question_chain = self.q_template | self.llm | StrOutputParser()
        
        # Explanation Generation
        self.e_template = PromptTemplate(
            input_variables=["context", "question", "correct_answer_text", "user_answer_text"],
            template="Explain why {correct_answer_text} is correct and not {user_answer_text} for the question: {question}. Use context: {context}. Keep it under 3 sentences."
        )
        self.explanation_chain = self.e_template | self.llm | StrOutputParser()

    def generate_question(self, difficulty="medium"):
        try:
            result = self.question_chain.invoke({"context": self.context, "difficulty": difficulty})
            return self._parse_question(result)
        except Exception as e:
            print(f"LLM Error: {e}")
            return None

    def _parse_question(self, text):
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        q_data = {"question": "", "options": {}, "correct_answer": "", "explanation": ""}
        for line in lines:
            if "QUESTION:" in line: q_data["question"] = line.split("QUESTION:")[1].strip()
            elif "A)" in line: q_data["options"]["A"] = line.split("A)")[1].strip()
            elif "B)" in line: q_data["options"]["B"] = line.split("B)")[1].strip()
            elif "C)" in line: q_data["options"]["C"] = line.split("C)")[1].strip()
            elif "D)" in line: q_data["options"]["D"] = line.split("D)")[1].strip()
            elif "ANSWER:" in line: q_data["correct_answer"] = line.split("ANSWER:")[1].strip()[0].upper()
            elif "EXPLANATION:" in line: q_data["explanation"] = line.split("EXPLANATION:")[1].strip()
        
        return q_data if q_data["question"] and len(q_data["options"]) == 4 else None

    def evaluate_answer(self, question, options, user_answer, correct_answer):
        is_correct = user_answer.upper() == correct_answer.upper()
        if is_correct:
            return {"is_correct": True, "message": "Correct!", "explanation": "", "correct_answer": correct_answer}
        
        try:
            explanation = self.explanation_chain.invoke({
                "context": self.context,
                "question": question,
                "correct_answer_text": options.get(correct_answer),
                "user_answer_text": options.get(user_answer)
            })
            return {"is_correct": False, "message": "Incorrect.", "explanation": explanation, "correct_answer": correct_answer}
        except:
            return {"is_correct": False, "message": "Incorrect.", "explanation": "Better luck next time!", "correct_answer": correct_answer}

    def get_properties(self):
        return self.properties