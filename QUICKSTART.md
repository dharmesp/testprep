# 🚀 Quick Start Guide

## Your Test Prep App is Ready!

The Flask server is currently running at: **http://127.0.0.1:5000**

## What You Can Do Now:

### 1. **Access the App**
   - Open your browser
   - Go to: `http://127.0.0.1:5000`
   - You'll see the login page

### 2. **Create Your Account**
   - Click on "Register here"
   - Enter username, email, and password
   - Click "Create Account"

### 3. **Create Your First Quiz**
   - After logging in, you'll see the Dashboard
   - Click "Create New Quiz" button
   - Enter a title (e.g., "Math Practice") and description
   - Click "Create Quiz"

### 4. **Add Questions with Images**
   - You'll be redirected to the Edit Quiz page
   - Use the form on the right to add questions:
     - Upload an image (the question)
     - Optionally enter the correct answer
     - Click "Add Question"
   - Repeat for all your questions

### 5. **Take a Quiz**
   - Go back to Dashboard
   - Click "Start Quiz" on any quiz
   - Answer each question in the text field
   - Click "Submit Quiz" when done

### 6. **Review Your Answers**
   - After submitting, you'll see the review page
   - Green = Correct, Red = Incorrect, Gray = Practice question
   - View your score and compare your answers

## Features Explained:

### ✅ **Optional Answers**
- When creating questions, you can leave the "Correct Answer" field blank
- These become practice questions (no grading)
- Great for open-ended questions or discussion prompts

### ✅ **Image-Based Questions**
- Supported formats: PNG, JPG, JPEG, GIF, WEBP
- Max file size: 16MB
- Perfect for math equations, diagrams, charts, etc.

### ✅ **Quiz Review**
- See all your past attempts in "Recent Attempts"
- Click "Review" to see your answers
- Compare with correct answers (when available)

### ✅ **Shared Quizzes**
- All users can take any quiz
- You can only edit quizzes you created
- Perfect for classroom or study group settings

## Stop/Restart the Server:

- **Stop**: Press `Ctrl+C` in the terminal
- **Restart**: Run `c:/webapp/training/.venv/Scripts/python.exe app.py`

## Troubleshooting:

1. **Can't upload images?**
   - Check file size (must be < 16MB)
   - Verify file format (PNG, JPG, JPEG, GIF, WEBP only)

2. **Server not responding?**
   - Make sure the server is running (check terminal)
   - Try refreshing the page
   - Check the URL: `http://127.0.0.1:5000`

3. **Forgot password?**
   - Currently no password reset (development mode)
   - You can delete the database file in `instance/` folder to start fresh

## What's Next?

Want to customize? Here are some ideas:
- Change colors in `templates/base.html` (inline CSS)
- Add time limits for quizzes
- Add categories or tags for quizzes
- Export quiz results to PDF
- Add multiple choice questions
- Add admin panel

---
**Happy Testing! 📚✨**
