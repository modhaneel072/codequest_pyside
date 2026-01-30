# CodeQuest - Interactive Python Learning Platform

A modern interactive Python learning platform built with **PySide6** for teaching programming through lessons, quizzes, coding challenges, and debugging exercises.

## Features

- **Interactive Lessons**: Step-by-step Python tutorials with explanations
- **Quizzes**: Multiple choice and free-response assessments
- **Coding Challenges**: Problem sets with automated grading
- **Debug Exercises**: Learn debugging by fixing code with error analysis
- **Terminal Access**: Execute Python code in a sandboxed environment
- **Progress Tracking**: Automatic progress saving

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/modhaneel072/codequest_pyside.git
   cd codequest_pyside
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

## Project Structure

```
src/
├── core/              # Core functionality
│   ├── content.py     # Content utilities
│   ├── io.py          # File I/O
│   ├── config.py      # Configuration management
│   ├── logging_config.py
│   └── ...
├── engine/            # Processing engine
│   ├── runner.py      # Code execution
│   ├── grading.py     # Grading
│   ├── content_loader.py
│   └── ...
├── pages/             # Page implementations
├── ui/                # UI components
├── widgets/           # Custom widgets
└── data/              # Data files (JSON)
```

## Technologies

- **Python 3.8+**: Core language
- **PySide6**: GUI framework
- **JSON**: Data storage
- **subprocess**: Code execution
- **logging**: Application logging

## Usage

Run the application:
```bash
python app.py
```

Navigate through:
1. Module selection
2. Interactive lessons
3. Quizzes and assessments
4. Coding challenges
5. Debugging exercises
6. Terminal for custom code execution

## Configuration

Application settings in `config.json`:
- Window dimensions
- Data paths
- Logging configuration
- Feature flags

## License

This project is provided for educational purposes.

## Repository

https://github.com/modhaneel072/codequest_pyside

