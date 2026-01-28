# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextBrowser
from src.core.progress import mark_completed, set_last_route

class LessonPage(QWidget):
    def __init__(self, nav, module_id: int, routes):
        super().__init__()
        self.nav = nav
        self.module_id = module_id
        self.routes = routes

        root = QVBoxLayout(self)
        top = QHBoxLayout()

        back = QPushButton("â† Back")
        back.clicked.connect(self.nav.go_back)

        title = QLabel(f"Module {module_id} Lesson")
        title.setStyleSheet("font-size: 18px; font-weight: 800;")

        top.addWidget(back); top.addStretch(1); top.addWidget(title); top.addStretch(1)
        root.addLayout(top)

        self.body = QTextBrowser()
        self.body.setMarkdown(self._lesson_markdown(module_id))
        root.addWidget(self.body)

        next_btn = QPushButton("Continue â†’ Quiz")
        next_btn.setMinimumHeight(44)
        next_btn.clicked.connect(self.complete_lesson)
        root.addWidget(next_btn)

        set_last_route("modules")

    def _lesson_markdown(self, module_id: int) -> str:
        return f"""
# Module {module_id}: Python Basics (Slow Mode)

## What you'll learn
- What Python is
- `print()` and simple output
- Variables (like labeled boxes)

## Example
```py
print("Hello, world!")
name = "Neel"
print("Hi", name)
```

## Mini-checkpoint
Before you continue, make sure you can explain:
- What `print()` does
- What a variable is
- Why strings need quotes
"""

    def complete_lesson(self):
        lesson_id = f"m{self.module_id}_lesson"
        mark_completed("lessons", lesson_id)
        self.routes["quiz"](quiz_id=f"m{self.module_id}_quiz")

