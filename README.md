# Test Prep Quiz App 📚

A lightweight, high-performance Flask-based web application for creating and taking image-based quizzes. Perfect for educational test preparation with support for unlimited questions, practice modes, and comprehensive review features.

---

## 🎯 Features

### Core Functionality
- ✅ **User Authentication** - Secure login and registration system
- ✅ **Quiz Management** - Create, edit, delete, and organize quiz sets
- ✅ **Image-Based Questions** - Upload or paste (Ctrl+V) images as questions
- ✅ **Flexible Grading** - Optional correct answers (some questions can be practice-only)
- ✅ **One-at-a-Time Quiz Taking** - Navigate questions with Next/Back buttons
- ✅ **Comprehensive Review** - Filter by correct/wrong/practice/unanswered
- ✅ **Export/Import** - Backup quizzes as ZIP files with images

### Performance Optimizations
- ⚡ **Pagination** - 20 questions per page (handles 1000+ questions easily)
- ⚡ **Lazy Image Loading** - Images load as you scroll
- ⚡ **Lightweight Review** - Table summary with click-to-view details
- ⚡ **Newest First** - Recently added questions appear on top

### User Experience
- 🎨 **Black & White Theme** - Clean, distraction-free interface
- 📱 **Responsive Design** - Optimized for widescreen and mobile (max 1600px)
- ⌨️ **Keyboard Shortcuts** - Alt+arrows for quiz navigation
- 🔄 **Attempt Management** - Delete individual attempts or clear all

---

## 🚀 Quick Start (Windows)

### Method 1: One-Click Install (Recommended)

1. **Download the repository**
   ```bash
   git clone https://github.com/dharmesp/testprep.git
   cd testprep
   ```

2. **Run the installer**
   ```bash
   install.bat
   ```

3. **Start the application**
   ```bash
   start.bat
   ```

4. **Open your browser** to http://127.0.0.1:5000

---

## 📋 Manual Installation (All Platforms)

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning)

### Step-by-Step Setup

#### 1. Download the Code
```bash
# Using Git
git clone https://github.com/dharmesp/testprep.git
cd testprep

# OR download ZIP from GitHub and extract
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Run the Application
```bash
python app.py
```

#### 5. Access the App
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📖 User Guide

### First Time Setup

1. **Register an Account**
   - Click "Register" on the login page
   - Enter username, email, and password
   - Login with your credentials

### Creating Your First Quiz

1. **Create Quiz**
   - Click "Create Quiz" from dashboard
   - Enter title (e.g., "NEC 2023 Code Changes")
   - Add description (optional)

2. **Add Questions**
   - Click "Edit" on your quiz
   - Upload question images (PNG, JPG, GIF, WEBP)
   - **Pro Tip**: Use Ctrl+V to paste images from clipboard!
   - Enter correct answer (or leave blank for practice)

3. **Question Types**
   - **Graded**: Enter correct answer → counts toward score
   - **Practice**: Leave answer blank → no scoring

### Taking a Quiz

1. Click "Start" on any quiz
2. Read question and type your answer
3. Navigate with **Next/Back** buttons or **Alt+Arrow keys**
4. View progress bar at top
5. Submit when complete

### Reviewing Results

1. **Summary View**
   - See overall score and statistics
   - Filter questions by: All/Correct/Wrong/Unanswered/Practice
   - Click "View" to see individual questions

2. **Question Detail**
   - View your answer vs. correct answer
   - Navigate between questions with arrows
   - Use keyboard shortcuts (arrow keys)

### Quiz Management

- **Export Quiz** - Download as ZIP (includes images)
- **Import Quiz** - Upload ZIP to restore
- **Export All** - Backup all your quizzes
- **Delete Quiz** - Remove quiz and all questions
- **Delete Attempts** - Clear quiz history

---

## 🛠️ Technical Details

### Technology Stack
- **Backend**: Flask 3.0.0
- **Database**: SQLite with SQLAlchemy 3.1.1
- **Authentication**: Werkzeug 3.0.1 (password hashing)
- **Frontend**: HTML, CSS, JavaScript (no frameworks)

### Project Structure
```
testprep/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── install.bat           # Windows installer
├── start.bat             # Windows launcher
├── templates/            # HTML templates
│   ├── base.html         # Base template with navbar
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Main dashboard
│   ├── create_quiz.html  # Quiz creation
│   ├── edit_quiz.html    # Quiz editing (with pagination)
│   ├── take_quiz.html    # Quiz taking interface
│   ├── review_quiz.html  # Review summary
│   └── review_question.html # Question detail view
├── static/
│   └── uploads/          # Question images (excluded from Git)
└── instance/
    └── testprep.db       # SQLite database (excluded from Git)
```

### Database Schema
- **User**: username, email, password_hash
- **Quiz**: title, description, created_by
- **Question**: quiz_id, image_path, correct_answer, order
- **QuizAttempt**: user_id, quiz_id, started_at, completed_at
- **Answer**: attempt_id, question_id, user_answer

---

## 🔧 Configuration

### Change Server Port
Edit `app.py` (bottom of file):
```python
if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Change to your port
```

### Change Upload Limits
Edit `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

### Pagination Settings
Edit `app.py` in `edit_quiz()` function:
```python
per_page = 50  # Change from 20 to 50 questions per page
```

### Secret Key (IMPORTANT for Production)
Edit `app.py`:
```python
app.config['SECRET_KEY'] = 'your-unique-secret-key-here'
```

---

## 🐛 Troubleshooting

### Virtual Environment Not Activating
```bash
# Windows: Run PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then retry install.bat
```

### Port Already in Use
```bash
# Change port in app.py or stop other Flask apps
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### Database Errors
```bash
# Delete and recreate database
rm instance/testprep.db
# Restart app - database will be recreated
```

### Image Upload Fails
- Check file size (max 16MB by default)
- Ensure `static/uploads/` folder exists
- Verify file extension is allowed (PNG, JPG, JPEG, GIF, WEBP)

### Module Not Found Errors
```bash
# Ensure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📝 Tips & Best Practices

### For Quiz Creators
- ✅ Use clear, high-quality images for questions
- ✅ Mark practice questions by leaving answer blank
- ✅ Export quizzes regularly as backups
- ✅ Use descriptive quiz titles and descriptions
- ✅ Organize questions logically (newest appear first)

### For Test Takers
- ✅ Review incorrect answers to learn
- ✅ Use filter buttons to focus on weak areas
- ✅ Try quizzes multiple times to track improvement
- ✅ Use keyboard shortcuts for faster navigation
- ✅ Delete practice attempts to keep history clean

### Performance Tips
- 📊 Pagination handles 1000+ questions efficiently
- 📊 Lazy loading reduces initial page load time
- 📊 Export/Import uses ZIP compression for efficiency
- 📊 Review page shows table summary (lightweight)

---

## 🔐 Security Notes

### For Development
- Default SECRET_KEY is included for convenience
- SQLite database stored locally
- No external connections required

### For Production Deployment
⚠️ **MUST DO before deploying:**
1. Change `SECRET_KEY` to a random string
2. Set `debug=False` in `app.run()`
3. Use a production WSGI server (e.g., Gunicorn, uWSGI)
4. Use PostgreSQL or MySQL instead of SQLite
5. Enable HTTPS
6. Add rate limiting
7. Configure proper file upload limits

---

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

---

## 📄 License

This project is open source. Use it freely for educational purposes.

---

## 🆘 Support

### Common Questions

**Q: Can multiple users share quizzes?**  
A: Yes! All quizzes are visible to all users (collaborative learning).

**Q: How many questions can a quiz have?**  
A: Unlimited! Pagination handles thousands of questions efficiently.

**Q: Can I edit questions after creating them?**  
A: Yes, delete and re-add questions as needed.

**Q: What happens to images when I delete a quiz?**  
A: All associated images are automatically deleted.

**Q: Can I export my data?**  
A: Yes! Export individual quizzes or all quizzes as ZIP files.

**Q: Does this work offline?**  
A: Yes! It's a local application with no internet required.

---

## 🎓 Use Cases

- 📚 Educational test preparation
- 🔌 Electrical code study (NEC, CEC, etc.)
- 🏗️ Building code review
- 🏥 Medical exam prep
- 💼 Certification practice
- 📖 Language learning
- 🧮 Math problem practice
- 🔬 Science quiz creation

---

## 🚀 Future Enhancements (Potential)

- [ ] Timer mode for timed quizzes
- [ ] Question randomization
- [ ] Multiple choice support
- [ ] Statistics dashboard
- [ ] Study mode (flashcards)
- [ ] Quiz sharing via links
- [ ] Mobile app version
- [ ] Dark mode option

---

**Made with ❤️ for efficient test preparation**

Repository: https://github.com/dharmesp/testprep

---

### Quick Reference Commands

```bash
# Install
install.bat              # Windows one-click install

# Run
start.bat                # Windows one-click start
python app.py            # Manual start

# Development
pip freeze > requirements.txt    # Update dependencies
git add .                        # Stage changes
git commit -m "message"          # Commit
git push origin main             # Push to GitHub
```
