# 🏠 Real Estate Quiz/Tutor Bot

An interactive, AI-driven educational platform designed for the Real Estate domain. This application engages users in targeted assessments based on real-world property listings, using Large Language Models (LLMs) to generate questions and provide deep contextual explanations for learning.

## 🚀 Features

-   **Dynamic Quiz Generation**: Automatically generates Multiple Choice Questions (MCQs) based on a JSON database of property listings.
-   **AI-Powered Feedback**: Provides personalized, contextual explanations for incorrect answers to bridge knowledge gaps using the **Groq API**.
-   **LangChain Integration**: Uses LangChain's Expression Language (LCEL) for robust prompt management and LLM orchestration.
-   **Real-Time Progress**: Tracks user scores, percentages, and progress through a 5-question assessment.
-   **Modern Web Interface**: A clean, responsive UI built with Flask, HTML5, CSS3, and JavaScript.
-   **Property Explorer**: Users can review property details (price, features, locations) before starting the quiz.

## 🛠️ Tech Stack

-   **Backend**: Python, Flask
-   **AI Framework**: LangChain
-   **LLM API**: Groq (Model: `llama3-8b-8192`)
-   **Environment Management**: `python-dotenv`
-   **Frontend**: HTML, CSS

## 📁 Project Structure

```text
real-estate-tutor-bot/
│
├── app.py              # Flask application routes and session management
├── .env                # API Keys (Excluded from Version Control)
├── property_data.json  # Raw data for property listings
├── requirements.txt    # Python dependencies
├── models/
│   ├── __init__.py
│   └── quiz_bot.py     # LangChain logic and Groq integration
├── static/
│   ├── css/
│   │   └── style.css   # Custom styling and animations
│   └── js/
│       └── main.js     # Frontend logic and API calls
└── templates/
    ├── base.html       # Shared layout template
    ├── index.html      # Home page (Property Listings)
    ├── quiz.html       # Interactive Quiz interface
    └── results.html    # Final performance summary
```

## ⚙️ Setup Instructions

### 1. Prerequisites
-   Python 3.8 or higher.
-   A Groq API Key (Get it at [console.groq.com](https://console.groq.com/)).

### 2. Installation
Clone the repository and navigate to the project folder:
```bash
git clone <your-repo-link>
cd real-estate-tutor-bot
```

### 3. Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory and add your API key:
```env
GROQ_API_KEY=your_gsk_api_key_here
```

### 6. Run the Application
```bash
python app.py
```
Open your browser and go to `http://localhost:5000`.

## 📝 Usage

1.  **Browse Properties**: On the home page, study the available property listings.
2.  **Start Quiz**: Click "Start Quiz" to begin an AI-generated 5-question assessment.
3.  **Submit Answers**: Select an option and submit.
4.  **Learn**: If you get an answer wrong, the bot will provide a "Tutor Explanation" explaining why the correct answer is right based on the property data.
5.  **View Results**: At the end, view your final score and performance summary.

## 🤖 AI Logic (LangChain)

The bot uses two main LangChain sequences:
1.  **Question Chain**: Takes property context and generates a structured MCQ.
2.  **Explanation Chain**: Triggered on wrong answers; it analyzes the user's choice vs. the correct choice and explains the real estate concept involved.

---
