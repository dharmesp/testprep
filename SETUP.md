# 🚀 QUICK SETUP GUIDE

## For New PC Installation (Windows)

### Method 1: Automated Install (Easiest) ⭐

1. **Download the project**
   - Go to: https://github.com/dharmesp/testprep
   - Click green "Code" button → "Download ZIP"
   - Extract ZIP to `C:\testprep` (or any folder)

2. **Double-click `install.bat`**
   - This will:
     ✓ Check Python installation
     ✓ Create virtual environment
     ✓ Install all dependencies
     ✓ Set up the application

3. **Double-click `start.bat`**
   - This will:
     ✓ Activate virtual environment
     ✓ Start the Flask server
     ✓ Open at http://127.0.0.1:5000

4. **Register and start creating quizzes!**

---

### Method 2: Manual Install (All Platforms)

#### Prerequisites
- Python 3.8+ installed and in PATH
- Internet connection (for downloading dependencies)

#### Steps

```bash
# 1. Download code
git clone https://github.com/dharmesp/testprep.git
cd testprep

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python app.py

# 6. Open browser to http://127.0.0.1:5000
```

---

## ✅ Verification Checklist

After installation, verify:
- [ ] Flask server starts without errors
- [ ] Browser opens to login page
- [ ] Can register new account
- [ ] Can create a quiz
- [ ] Can upload/paste images
- [ ] Can take a quiz
- [ ] Can review results

---

## ⚠️ Troubleshooting

### "Python is not recognized"
**Solution**: Install Python from https://www.python.org/
- ✓ Check "Add Python to PATH" during installation

### "pip is not recognized"
**Solution**: Reinstall Python with pip option checked

### Virtual environment won't activate (PowerShell)
**Solution**: Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port 5000 already in use
**Solution**: Kill the process or change port in app.py:
```python
app.run(debug=True, port=8080)  # Change to any free port
```

### Module not found errors
**Solution**: Ensure virtual environment is activated:
```bash
# You should see (.venv) in your terminal prompt
# If not, run activate command again
```

---

## 📁 What Gets Installed?

```
testprep/
├── .venv/                 # Virtual environment (300MB)
├── app.py                 # Main application
├── models.py              # Database models
├── requirements.txt       # Dependencies list
├── install.bat           # ⭐ Windows installer
├── start.bat             # ⭐ Windows launcher
├── README.md             # Full documentation
├── templates/            # HTML files
├── static/uploads/       # Question images (created on first run)
└── instance/testprep.db  # Database (created on first run)
```

---

## 🎯 First Steps After Installation

1. **Register Account**
   - Username: your_name
   - Email: your@email.com
   - Password: (secure password)

2. **Create First Quiz**
   - Click "Create Quiz"
   - Title: "Sample Quiz"
   - Description: "My first quiz"

3. **Add Questions**
   - Click "Edit" on your quiz
   - Upload/paste question images
   - Add correct answers (or leave blank)

4. **Take Quiz**
   - Click "Start"
   - Answer questions
   - Submit and review!

---

## 🔄 Daily Usage (Windows)

```bash
# Every time you want to use the app:
1. Double-click start.bat
2. Open browser to http://127.0.0.1:5000
3. Login and use!
4. Press Ctrl+C in terminal to stop server
```

---

## 📱 Access from Other Devices (Same Network)

1. Find your PC's IP address:
   ```bash
   ipconfig  # Windows
   # Look for IPv4 Address (e.g., 192.168.1.100)
   ```

2. Edit `app.py` (last line):
   ```python
   app.run(debug=True, host='0.0.0.0', port=5000)
   ```

3. Access from phone/tablet:
   ```
   http://192.168.1.100:5000
   ```

---

## 🔐 Important Notes

### Security
- ⚠️ Default SECRET_KEY is for development only
- ⚠️ Don't expose to internet without proper security
- ⚠️ Change SECRET_KEY before production use

### Data Storage
- Database: `instance/testprep.db`
- Images: `static/uploads/`
- Backup: Use Export All feature regularly

### System Requirements
- **Minimum**: 2GB RAM, 1GB free space
- **Recommended**: 4GB RAM, 2GB free space
- **OS**: Windows 7+, macOS 10.12+, Linux (any modern distro)

---

## 🆘 Getting Help

1. Check README.md for detailed documentation
2. Verify all prerequisites are installed
3. Ensure virtual environment is activated
4. Check console for error messages

---

**Ready to start? Run `install.bat` now!** 🚀
