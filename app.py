from flask import Flask, render_template, request, jsonify, session
from models.quiz_bot import RealEstateQuizBot
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Initialize quiz bot
try:
    quiz_bot = RealEstateQuizBot()
except Exception as e:
    print(f"❌ Failed to initialize Quiz Bot: {e}")
    quiz_bot = None

TOTAL_QUESTIONS = 5

@app.route('/')
def index():
    properties = quiz_bot.get_properties() if quiz_bot else []
    return render_template('index.html', properties=properties)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', total_questions=TOTAL_QUESTIONS)

@app.route('/api/start-quiz', methods=['POST'])
def start_quiz():
    session.clear()
    session['score'] = 0
    session['total_answered'] = 0
    session['question_number'] = 0
    return jsonify({"status": "success"})

@app.route('/api/get-question', methods=['GET'])
def get_question():
    if session.get('total_answered', 0) >= TOTAL_QUESTIONS:
        return jsonify({"error": "Quiz complete"}), 400
    
    print(f"Generating Question #{session.get('question_number', 0) + 1}...")
    
    question_data = quiz_bot.generate_question(difficulty="medium")
    
    if not question_data:
        print("❌ Error: Quiz Bot could not generate a question.")
        return jsonify({"error": "Failed to generate question"}), 500
    
    session['current_question'] = question_data['question']
    session['current_options'] = question_data['options']
    session['current_correct'] = question_data['correct_answer']
    session['question_number'] = session.get('question_number', 0) + 1
    
    return jsonify({
        "question_number": session['question_number'],
        "total_questions": TOTAL_QUESTIONS,
        "question": question_data['question'],
        "options": question_data['options']
    })

@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    user_answer = data.get('answer', '').upper()
    
    result = quiz_bot.evaluate_answer(
        session['current_question'],
        session['current_options'],
        user_answer,
        session['current_correct']
    )
    
    session['total_answered'] = session.get('total_answered', 0) + 1
    if result['is_correct']:
        session['score'] = session.get('score', 0) + 1
    
    return jsonify({
        "is_correct": result['is_correct'],
        "message": result['message'],
        "explanation": result['explanation'],
        "correct_answer": result['correct_answer'],
        "score": session['score'],
        "total_answered": session['total_answered']
    })

@app.route('/api/get-score', methods=['GET'])
def get_score():
    return jsonify({
        "score": session.get('score', 0),
        "total_answered": session.get('total_answered', 0),
        "total_questions": TOTAL_QUESTIONS
    })

@app.route('/results')
def results():
    score = session.get('score', 0)
    total = session.get('total_answered', 0)
    percentage = round((score / total) * 100, 1) if total > 0 else 0
    return render_template('results.html', score=score, total=total, percentage=percentage)

if __name__ == '__main__':
    app.run(debug=True, port=5000)