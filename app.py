from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
import json
import zipfile
from io import BytesIO
from datetime import datetime
from models import db, User, Quiz, Question, QuizAttempt, Answer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testprep.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize database
db.init_app(app)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ========== AUTHENTICATION ROUTES ==========

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ========== DASHBOARD ==========

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    quizzes = Quiz.query.all()
    recent_attempts = QuizAttempt.query.filter_by(user_id=user_id).order_by(QuizAttempt.completed_at.desc()).limit(5).all()
    return render_template('dashboard.html', quizzes=quizzes, recent_attempts=recent_attempts)

# ========== QUIZ MANAGEMENT ==========

@app.route('/create-quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        quiz = Quiz(
            title=title,
            description=description,
            created_by=session['user_id']
        )
        db.session.add(quiz)
        db.session.commit()
        
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('edit_quiz', quiz_id=quiz.id))
    
    return render_template('create_quiz.html')

@app.route('/quiz/<int:quiz_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Pagination - 20 questions per page
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Query questions in reverse order (newest first) with pagination
    pagination = Question.query.filter_by(quiz_id=quiz_id)\
        .order_by(Question.id.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    questions = pagination.items
    total_questions = Question.query.filter_by(quiz_id=quiz_id).count()
    
    return render_template('edit_quiz.html', 
                          quiz=quiz, 
                          questions=questions,
                          pagination=pagination,
                          total_questions=total_questions)

@app.route('/quiz/<int:quiz_id>/add-question', methods=['POST'])
@login_required
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Handle image upload
    if 'image' not in request.files:
        flash('No image uploaded.', 'danger')
        return redirect(url_for('edit_quiz', quiz_id=quiz_id))
    
    file = request.files['image']
    if file.filename == '':
        flash('No image selected.', 'danger')
        return redirect(url_for('edit_quiz', quiz_id=quiz_id))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid conflicts
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        
        # Get the next order number
        max_order = db.session.query(db.func.max(Question.order)).filter_by(quiz_id=quiz_id).scalar() or 0
        
        question = Question(
            quiz_id=quiz_id,
            image_path=filename,
            correct_answer=request.form.get('correct_answer'),  # Optional
            order=max_order + 1
        )
        db.session.add(question)
        db.session.commit()
        
        flash('Question added successfully!', 'success')
    else:
        flash('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, WEBP).', 'danger')
    
    return redirect(url_for('edit_quiz', quiz_id=quiz_id))

@app.route('/question/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    
    # Delete the image file
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], question.image_path)
    if os.path.exists(image_path):
        os.remove(image_path)
    
    db.session.delete(question)
    db.session.commit()
    
    flash('Question deleted.', 'info')
    return redirect(url_for('edit_quiz', quiz_id=quiz_id))

@app.route('/quiz/<int:quiz_id>/delete', methods=['POST'])
@login_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Check if user owns this quiz
    if quiz.created_by != session['user_id']:
        flash('You can only delete your own quizzes.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Delete all question images
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    for question in questions:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], question.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    # Delete the quiz (cascade will delete questions, attempts, and answers)
    db.session.delete(quiz)
    db.session.commit()
    
    flash('Quiz deleted successfully.', 'success')
    return redirect(url_for('dashboard'))

# ========== DELETE ATTEMPTS ==========

@app.route('/attempt/<int:attempt_id>/delete', methods=['POST'])
@login_required
def delete_attempt(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    
    # Check if user owns this attempt
    if attempt.user_id != session['user_id']:
        flash('You can only delete your own attempts.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Delete the attempt (cascade will delete answers)
    db.session.delete(attempt)
    db.session.commit()
    
    flash('Attempt deleted successfully.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/attempts/clear-all', methods=['POST'])
@login_required
def clear_all_attempts():
    # Delete all attempts for current user
    attempts = QuizAttempt.query.filter_by(user_id=session['user_id']).all()
    
    for attempt in attempts:
        db.session.delete(attempt)
    
    db.session.commit()
    
    flash(f'Cleared {len(attempts)} attempt(s) successfully.', 'success')
    return redirect(url_for('dashboard'))

# ========== TAKE QUIZ ==========

@app.route('/quiz/<int:quiz_id>/take')
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.order).all()
    
    if not questions:
        flash('This quiz has no questions yet.', 'warning')
        return redirect(url_for('dashboard'))
    
    # Create a new attempt
    attempt = QuizAttempt(
        user_id=session['user_id'],
        quiz_id=quiz_id,
        started_at=datetime.utcnow()
    )
    db.session.add(attempt)
    db.session.commit()
    
    return render_template('take_quiz.html', quiz=quiz, questions=questions, attempt_id=attempt.id)

@app.route('/quiz/submit/<int:attempt_id>', methods=['POST'])
@login_required
def submit_quiz(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    
    # Save answers
    for key, value in request.form.items():
        if key.startswith('answer_'):
            question_id = int(key.split('_')[1])
            answer = Answer(
                attempt_id=attempt_id,
                question_id=question_id,
                user_answer=value
            )
            db.session.add(answer)
    
    attempt.completed_at = datetime.utcnow()
    db.session.commit()
    
    flash('Quiz submitted successfully!', 'success')
    return redirect(url_for('review_quiz', attempt_id=attempt_id))

# ========== REVIEW QUIZ ==========

@app.route('/quiz/review/<int:attempt_id>')
@login_required
def review_quiz(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    
    if attempt.user_id != session['user_id']:
        flash('You cannot view this attempt.', 'danger')
        return redirect(url_for('dashboard'))
    
    answers = Answer.query.filter_by(attempt_id=attempt_id).all()
    questions = Question.query.filter_by(quiz_id=attempt.quiz_id).order_by(Question.order).all()
    
    # Create a dictionary of answers for easy lookup
    answer_dict = {answer.question_id: answer for answer in answers}
    
    # Calculate results for each question
    question_results = []
    correct_answers = 0
    wrong_answers = 0
    unanswered_count = 0
    practice_count = 0
    
    for idx, question in enumerate(questions):
        result = {
            'number': idx + 1,
            'question_id': question.id,
            'has_answer': question.id in answer_dict and answer_dict[question.id].user_answer,
            'is_correct': None,
            'is_practice': not question.correct_answer
        }
        
        if question.correct_answer and question.id in answer_dict:
            user_answer = answer_dict[question.id].user_answer
            if user_answer:
                is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
                result['is_correct'] = is_correct
                if is_correct:
                    correct_answers += 1
                else:
                    wrong_answers += 1
            else:
                unanswered_count += 1
        elif not question.correct_answer:
            practice_count += 1
        else:
            unanswered_count += 1
        
        question_results.append(result)
    
    return render_template('review_quiz.html', 
                          attempt=attempt, 
                          question_results=question_results,
                          total_questions=len(questions),
                          correct_answers=correct_answers,
                          wrong_answers=wrong_answers,
                          unanswered_count=unanswered_count,
                          practice_count=practice_count)

@app.route('/quiz/review/<int:attempt_id>/question/<int:question_number>')
@login_required
def review_question(attempt_id, question_number):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    
    if attempt.user_id != session['user_id']:
        flash('You cannot view this attempt.', 'danger')
        return redirect(url_for('dashboard'))
    
    questions = Question.query.filter_by(quiz_id=attempt.quiz_id).order_by(Question.order).all()
    
    if question_number < 1 or question_number > len(questions):
        flash('Invalid question number.', 'danger')
        return redirect(url_for('review_quiz', attempt_id=attempt_id))
    
    question = questions[question_number - 1]
    answer = Answer.query.filter_by(attempt_id=attempt_id, question_id=question.id).first()
    
    # Calculate if correct
    is_correct = None
    if question.correct_answer and answer and answer.user_answer:
        is_correct = answer.user_answer.strip().lower() == question.correct_answer.strip().lower()
    
    return render_template('review_question.html',
                          attempt=attempt,
                          question=question,
                          answer=answer,
                          question_number=question_number,
                          total_questions=len(questions),
                          is_correct=is_correct)

# ========== EXPORT / IMPORT QUIZ ==========

@app.route('/quiz/<int:quiz_id>/export')
@login_required
def export_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.order).all()
    
    # Create in-memory ZIP file
    memory_file = BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Prepare quiz data
        quiz_data = {
            'title': quiz.title,
            'description': quiz.description,
            'created_at': quiz.created_at.isoformat(),
            'questions': []
        }
        
        # Add questions and their images
        for idx, question in enumerate(questions):
            question_data = {
                'order': question.order,
                'correct_answer': question.correct_answer,
                'image_filename': f"question_{idx + 1}_{question.image_path}"
            }
            quiz_data['questions'].append(question_data)
            
            # Add image to ZIP
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], question.image_path)
            if os.path.exists(image_path):
                zf.write(image_path, f"images/{question_data['image_filename']}")
        
        # Add quiz metadata as JSON
        zf.writestr('quiz_data.json', json.dumps(quiz_data, indent=2))
    
    memory_file.seek(0)
    
    # Generate filename
    safe_title = "".join(c for c in quiz.title if c.isalnum() or c in (' ', '-', '_')).strip()
    filename = f"{safe_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=filename
    )

@app.route('/quiz/import', methods=['GET', 'POST'])
@login_required
def import_quiz():
    if request.method == 'POST':
        if 'quiz_file' not in request.files:
            flash('No file uploaded.', 'danger')
            return redirect(url_for('import_quiz'))
        
        file = request.files['quiz_file']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('import_quiz'))
        
        if not file.filename.endswith('.zip'):
            flash('Please upload a ZIP file.', 'danger')
            return redirect(url_for('import_quiz'))
        
        try:
            # Read ZIP file
            zip_data = BytesIO(file.read())
            
            with zipfile.ZipFile(zip_data, 'r') as zf:
                # Check if it's a single quiz or multiple quizzes backup
                file_list = zf.namelist()
                
                if 'all_quizzes_data.json' in file_list:
                    # Multiple quizzes backup
                    quizzes_json = zf.read('all_quizzes_data.json').decode('utf-8')
                    all_quizzes = json.loads(quizzes_json)
                    
                    imported_count = 0
                    for quiz_data in all_quizzes:
                        # Create new quiz
                        new_quiz = Quiz(
                            title=quiz_data['title'] + ' (Imported)',
                            description=quiz_data.get('description', ''),
                            created_by=session['user_id']
                        )
                        db.session.add(new_quiz)
                        db.session.flush()
                        
                        # Create questions and extract images
                        for q_data in quiz_data['questions']:
                            image_filename = q_data['image_filename']
                            image_data = zf.read(f"images/{image_filename}")
                            
                            new_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(image_filename)}"
                            image_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                            
                            with open(image_path, 'wb') as img_file:
                                img_file.write(image_data)
                            
                            question = Question(
                                quiz_id=new_quiz.id,
                                image_path=new_filename,
                                correct_answer=q_data.get('correct_answer'),
                                order=q_data.get('order', 0)
                            )
                            db.session.add(question)
                        
                        imported_count += 1
                    
                    db.session.commit()
                    flash(f'Successfully imported {imported_count} quiz(es)!', 'success')
                    return redirect(url_for('dashboard'))
                    
                elif 'quiz_data.json' in file_list:
                    # Single quiz backup
                    quiz_json = zf.read('quiz_data.json').decode('utf-8')
                    quiz_data = json.loads(quiz_json)
                    
                    # Create new quiz
                    new_quiz = Quiz(
                        title=quiz_data['title'] + ' (Imported)',
                        description=quiz_data.get('description', ''),
                        created_by=session['user_id']
                    )
                    db.session.add(new_quiz)
                    db.session.flush()
                    
                    # Create questions and extract images
                    for q_data in quiz_data['questions']:
                        image_filename = q_data['image_filename']
                        image_data = zf.read(f"images/{image_filename}")
                        
                        new_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(image_filename)}"
                        image_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                        
                        with open(image_path, 'wb') as img_file:
                            img_file.write(image_data)
                        
                        question = Question(
                            quiz_id=new_quiz.id,
                            image_path=new_filename,
                            correct_answer=q_data.get('correct_answer'),
                            order=q_data.get('order', 0)
                        )
                        db.session.add(question)
                    
                    db.session.commit()
                    flash(f'Quiz "{new_quiz.title}" imported successfully!', 'success')
                    return redirect(url_for('edit_quiz', quiz_id=new_quiz.id))
                else:
                    flash('Invalid quiz backup file format.', 'danger')
                    return redirect(url_for('import_quiz'))
                
        except Exception as e:
            db.session.rollback()
            flash(f'Error importing quiz: {str(e)}', 'danger')
            return redirect(url_for('import_quiz'))
    
    return render_template('import_quiz.html')

@app.route('/export-all-quizzes')
@login_required
def export_all_quizzes():
    """Export all quizzes created by the current user"""
    user_quizzes = Quiz.query.filter_by(created_by=session['user_id']).all()
    
    if not user_quizzes:
        flash('You have no quizzes to export.', 'warning')
        return redirect(url_for('dashboard'))
    
    # Create in-memory ZIP file
    memory_file = BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        all_quizzes_data = []
        
        for quiz in user_quizzes:
            questions = Question.query.filter_by(quiz_id=quiz.id).order_by(Question.order).all()
            
            quiz_data = {
                'title': quiz.title,
                'description': quiz.description,
                'created_at': quiz.created_at.isoformat(),
                'questions': []
            }
            
            # Add questions and their images
            for idx, question in enumerate(questions):
                question_data = {
                    'order': question.order,
                    'correct_answer': question.correct_answer,
                    'image_filename': f"quiz_{quiz.id}_question_{idx + 1}_{question.image_path}"
                }
                quiz_data['questions'].append(question_data)
                
                # Add image to ZIP
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], question.image_path)
                if os.path.exists(image_path):
                    zf.write(image_path, f"images/{question_data['image_filename']}")
            
            all_quizzes_data.append(quiz_data)
        
        # Add all quizzes metadata as JSON
        zf.writestr('all_quizzes_data.json', json.dumps(all_quizzes_data, indent=2))
    
    memory_file.seek(0)
    
    filename = f"all_quizzes_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=filename
    )

# ========== INITIALIZE DATABASE ==========

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
