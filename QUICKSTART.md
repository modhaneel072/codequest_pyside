# Quick Start Guide

Get CodeQuest running in 5 minutes!

## Step 1: Clone/Download Project
```bash
cd codequest_pyside
```

## Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

## Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 4: Run Application
```bash
python app.py
```

The CodeQuest window will open. Click **Start Course** to begin learning Python!

---

## What's Inside?

- **Module 1**: Python Basics (print, strings, variables)
- **Module 2**: Control Flow (if, loops)
- And more...

Each module includes:
- Interactive lessons
- Code examples to try
- Quizzes to test your knowledge
- Problem sets to practice

## Troubleshooting

### Python not found
Make sure Python 3.8+ is installed:
```bash
python --version
```

### Can't activate virtual environment
Use the correct activation script:
- **Windows**: `.venv\Scripts\activate`
- **macOS/Linux**: `source .venv/bin/activate`

### Import errors
Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. **Start Learning**: Click "Start Course" in the app
2. **Read Documentation**: Check [README.md](README.md) for full guide
3. **Explore Code**: See [DEVELOPMENT.md](DEVELOPMENT.md) for architecture
4. **Customize**: Edit [config.json](config.json) for settings

## Need Help?

1. Check the [README.md](README.md) troubleshooting section
2. Review the [DEVELOPMENT.md](DEVELOPMENT.md) guide
3. Check application logs in `logs/codequest.log`

Enjoy learning Python with CodeQuest! 🚀
