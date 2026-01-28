# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup, QMessageBox, QScrollArea
from src.core.io import load_json
from src.core.quiz import grade_quiz
from src.core.progress import mark_completed, set_last_route

class QuizPage(QWidget):
    def __init__(self, nav, quiz_id: str, routes, on_pass=None):
        super().__init__()
        self.nav = nav
        self.routes = routes
        self.on_pass = on_pass
        self.spec = load_json(f"src/data/quizzes/{quiz_id}.json")
        self.quiz_id = quiz_id
        self.groups = []

        root = QVBoxLayout(self)

        top = QHBoxLayout()
        back = QPushButton("← Back")
        back.clicked.connect(self.nav.go_back)
        title = QLabel(self.spec.get("title", "Quiz"))
        title.setStyleSheet("font-size:18px; font-weight:800;")
        top.addWidget(back); top.addStretch(1); top.addWidget(title); top.addStretch(1)
        root.addLayout(top)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        body = QVBoxLayout(container)

        for idx, q in enumerate(self.spec.get("questions", []), start=1):
            qlbl = QLabel(f"{idx}. {q['prompt']}")
            qlbl.setWordWrap(True)
            qlbl.setStyleSheet("font-weight:700; margin-top:10px;")
            body.addWidget(qlbl)

            group = QButtonGroup(self)
            self.groups.append(group)

            for ci, choice in enumerate(q["choices"]):
                rb = QRadioButton(choice)
                group.addButton(rb, ci)
                body.addWidget(rb)

        body.addStretch(1)
        scroll.setWidget(container)
        root.addWidget(scroll)

        submit = QPushButton("Submit Quiz")
        submit.setMinimumHeight(44)
        submit.clicked.connect(self.submit_quiz)
        root.addWidget(submit)

        set_last_route("modules")

    def submit_quiz(self):
        answers = []
        for g in self.groups:
            answers.append(g.checkedId())

        # if any unanswered, checkedId() == -1
        if any(a == -1 for a in answers):
            QMessageBox.warning(self, "Incomplete", "Answer all questions first.")
            return

        passed, score, msg = grade_quiz(self.spec, answers)
        if passed:
            mark_completed("quizzes", self.quiz_id)
            QMessageBox.information(self, "Passed", f"✅ Passed! {msg}")
            if callable(self.on_pass):
                self.on_pass()
        else:
            QMessageBox.warning(self, "Try again", f"❌ Not passed. {msg}\nReview the lesson and retry.")
