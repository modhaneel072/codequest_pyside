# CodeQuest Development Guide

This guide helps developers understand the codebase and contribute to CodeQuest.

## Architecture Overview

### Core Layers

1. **Data Layer** (`src/data/`)
   - JSON-based content storage
   - Course definitions, lessons, quizzes, problems
   - User progress tracking

2. **Engine Layer** (`src/engine/`)
   - Business logic: content loading, grading, code execution
   - State management
   - Progress tracking

3. **UI Layer** (`src/ui/`)
   - PySide6-based GUI components
   - Main window, pages, transitions
   - Widget styling

4. **Core Utilities** (`src/core/`)
   - Configuration management
   - Logging setup
   - File I/O with error handling
   - Progress persistence

### Key Design Patterns

#### 1. Configuration Management
Use the `Config` singleton from `src/core/config.py`:
```python
from src.core.config import get_config

config = get_config()
timeout = config.get('code_execution.timeout_seconds')
config.set('app.title', 'New Title')
```

#### 2. Logging
Always use logging instead of print:
```python
import logging
logger = logging.getLogger(__name__)

logger.info("User completed module 1")
logger.warning("Quiz file not found")
logger.error("Failed to save progress", exc_info=True)
```

#### 3. Error Handling
Always validate inputs and handle errors gracefully:
```python
def load_content(content_id: str) -> Dict[str, Any]:
    """Load content with error handling."""
    if not content_id or not isinstance(content_id, str):
        logger.error(f"Invalid content_id: {content_id}")
        raise ValueError(f"Invalid content_id: {content_id}")
    
    try:
        # Load logic here
        pass
    except FileNotFoundError as e:
        logger.error(f"Content file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        raise
```

#### 4. Type Hints
Always use type hints for better code clarity:
```python
from typing import Dict, List, Optional, Tuple, Any

def grade_quiz(
    quiz: Dict[str, Any],
    answers: Dict[str, Any]
) -> Tuple[int, Dict[str, Any]]:
    """Grade a quiz and return (score, details)."""
    pass
```

## Module Guide

### src/core/config.py
**Purpose:** Centralized configuration management

Key classes:
- `Config` - Configuration manager with dot-notation access

Example usage:
```python
config = get_config()
# Read
score = config.get('grading.passing_score')  # Returns 90
# Write
config.set('grading.passing_score', 85)
# Save
config.save('config.json')
```

### src/core/logging_config.py
**Purpose:** Logging setup and configuration

Key functions:
- `setup_logging()` - Initialize logging system
- `get_logger()` - Get logger for module

Example:
```python
from src.core.logging_config import setup_logging, get_logger

setup_logging(level=logging.DEBUG, log_file='debug.log')
logger = get_logger(__name__)
```

### src/engine/runner.py
**Purpose:** Execute user Python code safely

Key classes:
- `RunResult` - Dataclass containing execution results

Key functions:
- `run_python(code: str, timeout_sec: float) -> RunResult`

Example:
```python
from src.engine.runner import run_python

result = run_python("print('Hello')", timeout_sec=2.0)
if result.ok:
    print(result.stdout)
else:
    print(result.stderr)
```

### src/engine/grading.py
**Purpose:** Quiz grading logic

Key functions:
- `grade_quiz(quiz, answers) -> Tuple[int, Dict]`
- `passed(score, passing_score=90) -> bool`

Example:
```python
from src.engine.grading import grade_quiz, passed

points, details = grade_quiz(quiz_def, user_answers)
if passed(points):
    print("Quiz passed!")
```

### src/core/content.py
**Purpose:** Content loading with error handling

Key functions:
- `load_lesson(path: str) -> str`
- `load_problem(problem_id: str, base_dir: str) -> Dict`

Example:
```python
from src.core.content import load_lesson, load_problem

try:
    lesson = load_lesson("src/data/lessons/m1_1.md")
    problem = load_problem("m1_ps1")
except FileNotFoundError as e:
    logger.error(f"Content not found: {e}")
```

## Adding New Features

### Adding a New Page

1. Create a new page class in `src/pages/`:
```python
from PySide6.QtWidgets import QWidget

class MyNewPage(QWidget):
    def __init__(self, nav, routes):
        super().__init__()
        self.nav = nav
        self.routes = routes
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize UI components."""
        pass
```

2. Register in main.py:
```python
self.pages["my_page"] = MyNewPage(self.nav, routes)
self.stack.addWidget(self.pages["my_page"])
```

### Adding a Quiz

1. Create quiz definition in `src/data/quizzes/`:
```json
{
  "title": "Module 1 Quiz",
  "mcq": [
    {
      "question": "What is Python?",
      "choices": ["A language", "A snake", "Both"],
      "correct_index": 0
    }
  ],
  "frq": {
    "question": "Explain variables",
    "keywords": ["store", "reuse"],
    "expected_fix_contains": ["variable"]
  }
}
```

2. Load and grade in your code:
```python
quiz = load_json("src/data/quizzes/m1_quiz.json")
score, details = grade_quiz(quiz, user_answers)
```

### Adding Configuration Options

1. Update `DEFAULT_CONFIG` in `src/core/config.py`
2. Use in code:
```python
config = get_config()
my_value = config.get('section.option', default_value)
```

## Testing Guidelines

### Unit Test Structure
```python
import unittest
from src.engine.grading import grade_quiz, passed

class TestGrading(unittest.TestCase):
    def test_passing_score(self):
        self.assertTrue(passed(95))
        self.assertFalse(passed(80))
    
    def test_grade_quiz(self):
        quiz = {"mcq": [...], "frq": {...}}
        answers = {"mcq": [...], "frq": "..."}
        score, details = grade_quiz(quiz, answers)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
```

### Running Tests
```bash
pytest tests/
pytest tests/test_grading.py -v  # Verbose
pytest tests/ -k "test_passing"  # Specific test
```

## Code Style Guidelines

### PEP 8 Compliance
- 4 spaces for indentation
- Lines max 100 characters
- Two blank lines between top-level classes/functions
- One blank line between methods

### Docstring Format
Use Google-style docstrings:
```python
def my_function(arg1: str, arg2: int) -> bool:
    """
    Brief description of function.
    
    Longer description if needed. Explain the purpose,
    parameters, return value, and any exceptions raised.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When arg1 is empty
        TypeError: When arg2 is not an integer
    """
    pass
```

### Type Hints
Always include type hints:
```python
from typing import Dict, List, Optional, Union, Tuple, Any

def process_data(
    items: List[str],
    config: Optional[Dict[str, Any]] = None
) -> Tuple[bool, Dict[str, Any]]:
    pass
```

## Debugging Tips

### Enable Debug Logging
```python
from src.core.logging_config import setup_logging
import logging

setup_logging(level=logging.DEBUG, log_file='debug.log')
```

### Inspect Configuration
```python
from src.core.config import get_config
config = get_config()
# Print all config
import json
print(json.dumps(config._config, indent=2))
```

### Trace Code Execution
```python
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Variable value: {variable}")
logger.debug(f"Function input: {arg1}, {arg2}")
```

### Check Logs
```bash
# Watch logs in real-time (Windows PowerShell)
Get-Content logs/codequest.log -Wait

# Or view last 50 lines
Get-Content logs/codequest.log -Tail 50
```

## Common Issues and Solutions

### Issue: Configuration not loading
**Solution:** Check that `config.json` is in project root and valid JSON
```bash
python -m json.tool config.json  # Validate JSON
```

### Issue: Logging not appearing
**Solution:** Call `setup_logging()` early in application startup
```python
from src.core.logging_config import setup_logging
setup_logging(level=logging.INFO, console=True)
```

### Issue: Code execution timeout
**Solution:** Increase timeout in `config.json` or check for infinite loops
```json
{
  "code_execution": {
    "timeout_seconds": 5.0
  }
}
```

### Issue: File not found errors
**Solution:** Always use absolute paths via `Path(__file__).parent`
```python
from pathlib import Path
data_dir = Path(__file__).resolve().parent.parent / "data"
```

## Performance Considerations

1. **Code Execution:** Use subprocess for isolation (already implemented)
2. **File I/O:** Cache frequently accessed data in memory
3. **UI Updates:** Use async operations for long-running tasks
4. **Progress Saving:** Batch writes to reduce disk I/O

## Security Best Practices

1. **Code Execution:** Always run user code in subprocess with timeout
2. **Input Validation:** Always validate quiz_id, problem_id, etc.
3. **File Access:** Use pathlib.Path for safe file operations
4. **Error Messages:** Don't expose system paths in user-facing errors

## Release Checklist

Before releasing a new version:
- [ ] Update version in `config.py`
- [ ] Update `requirements.txt` with tested versions
- [ ] Run all tests: `pytest tests/`
- [ ] Check code style: `pylint src/`
- [ ] Update `README.md` with new features
- [ ] Update `CHANGELOG.md`
- [ ] Tag release in git: `git tag v1.0.0`

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes with descriptive commits
3. Add tests for new functionality
4. Update documentation
5. Submit pull request with description

## Resources

- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [Type Hints](https://docs.python.org/3/library/typing.html)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
