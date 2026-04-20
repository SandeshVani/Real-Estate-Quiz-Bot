// ===================================
// GLOBAL VARIABLES
// ===================================

let currentQuestion = null;
let selectedAnswer = null;
const TOTAL_QUESTIONS = 5;

// ===================================
// INITIALIZATION
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    initializeQuiz();
});

async function initializeQuiz() {
    try {
        // Start quiz session
        await fetch('/api/start-quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Load first question
        await loadQuestion();
    } catch (error) {
        console.error('Initialization error:', error);
        showError('Failed to initialize quiz. Please refresh the page.');
    }
}

// ===================================
// QUESTION LOADING
// ===================================

async function loadQuestion() {
    try {
        // Show loading state
        showState('loading');
        selectedAnswer = null;

        // Fetch question from API
        const response = await fetch('/api/get-question');
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        currentQuestion = data;
        displayQuestion(data);

    } catch (error) {
        console.error('Error loading question:', error);
        
        // Check if quiz is complete
        const scoreResponse = await fetch('/api/get-score');
        const scoreData = await scoreResponse.json();
        
        if (scoreData.total_answered >= TOTAL_QUESTIONS) {
            window.location.href = '/results';
        } else {
            showError('Failed to load question. Please try again.');
        }
    }
}

function displayQuestion(data) {
    // Update question number
    document.getElementById('question-number').textContent = 
        `Question ${data.question_number} of ${TOTAL_QUESTIONS}`;

    // Update question text
    document.getElementById('question-text').textContent = data.question;

    // Create options
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';

    for (let [letter, text] of Object.entries(data.options)) {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option';
        optionDiv.onclick = () => selectOption(letter, optionDiv);
        
        optionDiv.innerHTML = `
            <div class="option-letter">${letter}</div>
            <div class="option-text">${text}</div>
        `;
        
        optionsContainer.appendChild(optionDiv);
    }

    // Reset submit button
    document.getElementById('submit-btn').disabled = true;

    // Show question state
    showState('question');

    // Update score
    updateScore();
}

// ===================================
// ANSWER SELECTION
// ===================================

function selectOption(letter, element) {
    // Remove previous selection
    document.querySelectorAll('.option').forEach(opt => {
        opt.classList.remove('selected');
    });

    // Add new selection
    element.classList.add('selected');
    selectedAnswer = letter;

    // Enable submit button
    document.getElementById('submit-btn').disabled = false;
}

// ===================================
// ANSWER SUBMISSION
// ===================================

async function submitAnswer() {
    if (!selectedAnswer) {
        return;
    }

    // Disable submit button
    document.getElementById('submit-btn').disabled = true;

    try {
        const response = await fetch('/api/submit-answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                answer: selectedAnswer
            })
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        displayFeedback(data);

    } catch (error) {
        console.error('Error submitting answer:', error);
        showError('Failed to submit answer. Please try again.');
        document.getElementById('submit-btn').disabled = false;
    }
}

// ===================================
// FEEDBACK DISPLAY
// ===================================

function displayFeedback(data) {
    const feedbackCard = document.getElementById('feedback-card');
    const feedbackTitle = document.getElementById('feedback-title');
    const feedbackMessage = document.getElementById('feedback-message');
    const explanationBox = document.getElementById('explanation-box');
    const nextBtn = document.getElementById('next-btn');
    const nextBtnText = document.getElementById('next-btn-text');

    // Set feedback style
    feedbackCard.className = 'feedback-card ' + (data.is_correct ? 'correct' : 'incorrect');

    // Set title
    feedbackTitle.textContent = data.is_correct ? '✅ Correct!' : '❌ Incorrect';

    // Set message
    feedbackMessage.textContent = data.message;

    // Set explanation
    if (data.explanation) {
        explanationBox.innerHTML = `
            <h3>💡 Explanation</h3>
            <p><strong>Correct Answer: ${data.correct_answer})</strong> ${currentQuestion.options[data.correct_answer]}</p>
            <p style="margin-top: 1rem;">${data.explanation}</p>
        `;
        explanationBox.style.display = 'block';
    } else {
        explanationBox.style.display = 'none';
    }

    // Update next button text
    if (data.total_answered >= TOTAL_QUESTIONS) {
        nextBtnText.textContent = 'View Results 🎯';
    } else {
        nextBtnText.textContent = 'Next Question →';
    }

    // Update score
    updateScore();

    // Show feedback state
    showState('feedback');
}

// ===================================
// NAVIGATION
// ===================================

async function nextQuestion() {
    try {
        const response = await fetch('/api/get-score');
        const data = await response.json();

        if (data.total_answered >= TOTAL_QUESTIONS) {
            // Quiz complete - redirect to results
            window.location.href = '/results';
        } else {
            // Load next question
            await loadQuestion();
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to proceed. Please try again.');
    }
}

// ===================================
// UI STATE MANAGEMENT
// ===================================

function showState(state) {
    const states = ['loading', 'question', 'feedback'];
    
    states.forEach(s => {
        const element = document.getElementById(`${s}-state`);
        if (element) {
            element.style.display = (s === state) ? 'block' : 'none';
        }
    });
}

// ===================================
// SCORE UPDATE
// ===================================

async function updateScore() {
    try {
        const response = await fetch('/api/get-score');
        const data = await response.json();

        document.getElementById('score').textContent = data.score;
        document.getElementById('total').textContent = data.total_answered;

        // Update percentage if element exists
        const percentageEl = document.getElementById('percentage');
        if (percentageEl && data.total_answered > 0) {
            const percentage = ((data.score / data.total_answered) * 100).toFixed(1);
            percentageEl.textContent = `(${percentage}%)`;
        }
    } catch (error) {
        console.error('Error updating score:', error);
    }
}

// ===================================
// ERROR HANDLING
// ===================================

function showError(message) {
    alert(message);
}

// ===================================
// HELPER FUNCTIONS
// ===================================

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}