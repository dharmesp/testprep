# Test Prep Web App 📚

A Flask-based web application for creating and taking image-based quizzes for test preparation.

## Features ✨

- **User Authentication**: Secure login and registration system
- **Quiz Management**: Create and edit quiz sets
- **Image Questions**: Upload images as questions
- **Flexible Answers**: Optional correct answers (some questions can be practice-only)
- **Review Mode**: Review your completed quizzes with scoring
- **Responsive Design**: Clean, modern interface

## Installation 🚀

1. **Activate the virtual environment** (already set up):
   ```bash
   .\app\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage 📖

### Getting Started
1. Register a new account
2. Login with your credentials
3. Create your first quiz from the dashboard

### Creating a Quiz
1. Click "Create New Quiz"
2. Enter quiz title and description
3. Add questions by uploading images
4. Optionally add correct answers (leave blank for practice questions)

### Taking a Quiz
1. Select a quiz from the dashboard
2. Answer each question in the text field
3. Submit when complete
4. Review your answers and see your score

### Reviewing Quizzes
- View all your completed quiz attempts
- See which questions you got right/wrong
- Compare your answers with correct answers (when available)

## Project Structure 📁

```
training/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create_quiz.html
│   ├── edit_quiz.html
│   ├── take_quiz.html
│   └── review_quiz.html
├── static/
│   └── uploads/          # Uploaded question images
└── testprep.db           # SQLite database (created on first run)
```

## Database Schema 💾

- **User**: User accounts
- **Quiz**: Quiz collections
- **Question**: Individual questions with images
- **QuizAttempt**: User's quiz attempts
- **Answer**: User's answers for each question

## Technologies Used 🛠️

- **Backend**: Flask (Python)
- **Database**: SQLite with Flask-SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **Security**: Werkzeug password hashing

## Notes 📝

- Maximum upload size: 16MB
- Supported image formats: PNG, JPG, JPEG, GIF, WEBP
- Questions can have optional correct answers for grading
- All quizzes are shared among users (collaborative learning)

## Security Reminder 🔒

Don't forget to change the `SECRET_KEY` in `app.py` before deploying to production!

---
Made with ❤️ for test preparation
