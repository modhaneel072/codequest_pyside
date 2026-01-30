# CodeQuest - Interactive Python Learning Platform

A desktop-based interactive Python learning application built with **PySide6**. CodeQuest teaches Python fundamentals through structured lessons, practice exercises, quizzes, and progress tracking.

## Features

✅ **Structured Learning Path** - Learn Python step-by-step through organized modules  
✅ **Interactive Lessons** - Read lessons with clear explanations and code examples  
✅ **Instant Feedback** - Get immediate feedback on quizzes and code submissions  
✅ **Progress Tracking** - Save and resume learning progress across sessions  
✅ **Code Execution** - Run and test Python code directly in the application  
✅ **Comprehensive Grading** - Auto-graded quizzes with detailed feedback  
✅ **Hackathons** - Challenge-based missions for advanced learners  

## Project Structure

```
codequest_pyside/
├── app.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── config.json                     # Application configuration (optional)
├── README.md                       # This file
├── src/
│   ├── main.py                     # Main window setup
│   ├── core/                       # Core utilities
│   │   ├── content.py              # Content loading
│   │   ├── config.py               # Configuration management
│   │   ├── logging_config.py       # Logging setup
│   │   ├── io.py                   # File I/O utilities
│   │   ├── nav.py                  # Navigation management
│   │   ├── progress.py             # Progress tracking
│   │   ├── grader.py               # Grading logic
│   │   ├── quiz.py                 # Quiz handling
│   │   └── debug.py                # Debug utilities
│   ├── engine/                     # Core application logic
│   │   ├── content_loader.py       # Load course/progress data
│   │   ├── runner.py               # Python code execution
│   │   ├── grading.py              # Quiz grading engine
│   │   ├── autograder.py           # Automatic grading
│   │   ├── state.py                # Application state
│   │   ├── progress.py             # Progress management
│   │   ├── lectures.py             # Lecture content
│   │   └── scaffold.py             # Code scaffolding
│   ├── pages/                      # Page/screen definitions
│   │   ├── boot.py                 # Boot/home page
│   │   ├── modules.py              # Modules overview
│   │   ├── lesson.py               # Lesson viewer
│   │   ├── quiz.py                 # Quiz interface
│   │   ├── problem_sets.py         # Problem sets
│   │   ├── debug.py                # Debug challenges
│   │   └── hackathons.py           # Hackathon challenges
│   ├── ui/                         # UI components
│   │   ├── main_window.py          # Main window
│   │   ├── boot_menu.py            # Boot menu
│   │   ├── pages.py                # Page components
│   │   ├── styles.py               # Styling (CSS-like)
│   │   ├── transitions.py          # Page transitions
│   │   └── code_editor.py          # Code editor widget
│   ├── widgets/                    # Custom widgets
│   │   ├── code_editor.py          # Code editor
│   │   └── __init__.py
│   └── data/                       # Content and progress data
│       ├── course.json             # Course structure
│       ├── progress.json           # User progress
│       ├── settings.json           # User settings
│       ├── lessons/                # Lesson Markdown files
│       ├── problems/               # Problem definitions
│       ├── quizzes/                # Quiz definitions
│       ├── debugs/                 # Debug challenge definitions
│       └── hackathons/             # Hackathon definitions
└── logs/                           # Application logs (created at runtime)
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the project**
   ```bash
   cd codequest_pyside
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python app.py
```

The application will launch with a boot menu displaying:
- **Continue** - Resume from your last session
- **Start Course** - Begin from Module 1
- **Modules** - Browse all available modules
- **Problem Sets** - Practice problem sets
- **Hackathons** - Challenge-based missions

## Configuration

### Optional: Custom Configuration

Create a `config.json` file in the project root to customize settings:

```json
{
  "app": {
    "title": "CodeQuest",
    "window_width": 1200,
    "window_height": 760
  },
  "code_execution": {
    "timeout_seconds": 2.0,
    "max_output_length": 5000
  },
  "grading": {
    "passing_score": 90,
    "mcq_points": 40
  },
  "logging": {
    "level": "INFO",
    "enable_file_logging": true,
    "log_file": "logs/codequest.log"
  }
}
```

All settings have sensible defaults, so this file is optional.

## Creating Lesson Content

### Lesson Format

Lessons are defined in `src/data/course.json`. Each module can contain:

```json
{
  "id": "m1",
  "title": "Module 1 - Python Basics",
  "objective": "Learn print(), strings, and variables",
  "sections": ["What is print()", "Strings", "Variables"],
  "lesson_html": "<h1>Module 1</h1><p>...</p>",
  "examples": [
    {
      "title": "Example: print()",
      "code": "print('Hello, Python!')",
      "task": "Run it and modify the text"
    }
  ],
  "quiz": {
    "mcq": [
      {
        "question": "What does this print?\nprint('Hi')",
        "choices": ["Hi", "hi", "print('Hi')", "(nothing)"],
        "correct_index": 0
      }
    ],
    "frq": {
      "question": "Explain why we use variables",
      "keywords": ["store", "reuse", "value"],
      "expected_fix_contains": ["variable"]
    }
  }
}
```

## Features in Detail

### Progress Tracking

Progress is automatically saved to `src/data/progress.json`:
```json
{
  "module_index": 2,
  "history": [
    {"module": "m1", "timestamp": "2024-01-30T10:30:00"},
    {"module": "m2", "timestamp": "2024-01-30T11:00:00"}
  ],
  "terminal_unlocked": {
    "commands": ["help", "status"]
  }
}
```

### Code Execution

- Code runs in a secure isolated subprocess with **2-second timeout**
- Stdout and stderr are captured
- Infinite loops are safely terminated
- All temporary files are cleaned up

### Quiz Grading

Quizzes use:
- **Multiple Choice:** 40 points each (80 points total)
- **Free Response:** 20 points with keyword matching
- **Passing Score:** 90 points
- **Partial Credit:** For free response questions based on keywords

## Error Handling

The application includes comprehensive error handling:

- **Missing Files:** Gracefully handled with informative error messages
- **Invalid JSON:** Automatic fallback to defaults
- **Code Execution Errors:** Captured and displayed to user
- **Network Issues:** Handled with appropriate UI feedback
- **Logging:** All errors logged to `logs/codequest.log`

## Logging

Logs are written to `logs/codequest.log` (automatically created). Log levels:
- **DEBUG:** Detailed developer information
- **INFO:** General informational messages
- **WARNING:** Warning messages
- **ERROR:** Error messages

To change log level, modify `config.json`:
```json
{
  "logging": {
    "level": "DEBUG"
  }
}
```

## Development

### Adding New Modules

1. Add module definition to `src/data/course.json`
2. Create lesson content
3. Create quiz definition
4. Create problem set (optional)
5. Test via the UI

### Running Tests

```bash
pytest tests/
```

### Code Style

The project follows PEP 8 guidelines:
- Use type hints for functions
- Add comprehensive docstrings
- Use logging instead of print statements
- Handle exceptions explicitly

## Troubleshooting

### Application Won't Start
1. Ensure Python 3.8+ is installed: `python --version`
2. Verify dependencies: `pip install -r requirements.txt`
3. Check logs: `tail -f logs/codequest.log`

### Missing Data Files
The application will display informative errors if data files are missing. Ensure:
- `src/data/course.json` exists
- All referenced modules have definitions

### Code Won't Execute
- Check syntax with Python: `python -m py_compile your_code.py`
- Verify timeout isn't too short (default: 2 seconds)
- Check application logs for details

## Contributing

Contributions are welcome! Please:
1. Follow the existing code style
2. Add docstrings and type hints
3. Update this README if adding features
4. Test changes before submitting

## License

This project is part of the CodeQuest learning platform.

## Support

For issues, questions, or suggestions:
1. Check the logs in `logs/codequest.log`
2. Review the code documentation
3. Ensure all data files are properly formatted JSON

## Version History

- **1.0.0** (January 2025) - Initial release with:
  - Module-based learning path
  - Interactive lessons and quizzes
  - Code execution environment
  - Progress tracking
  - Comprehensive error handling and logging

