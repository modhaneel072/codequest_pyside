# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QPushButton, QLabel, QSplitter, QMessageBox, QPlainTextEdit

from src.core.io import load_json
from src.core.grader import run_code_capture_stdout, grade_problem
from src.core.progress import mark_completed, set_last_route
from src.widgets.code_editor import CodeEditor

class ProblemSetPage(QWidget):
    def __init__(self, nav, problem_id="ps1_positive_checker", on_pass=None):
        super().__init__()
        self.nav = nav
        self.on_pass = on_pass
        self.spec = load_json(f"src/data/problems/{problem_id}.json")
        self.problem_id = problem_id

        root = QVBoxLayout(self)
        header = QHBoxLayout()

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.nav.go_back)

        title = QLabel(self.spec.get("title","Problem Sets"))
        title.setStyleSheet("font-size: 18px; font-weight: 700;")

        header.addWidget(back_btn)
        header.addStretch(1)
        header.addWidget(title)
        header.addStretch(1)

        root.addLayout(header)

        splitter = QSplitter(Qt.Horizontal)

        self.desc = QTextBrowser()
        self.desc.setMarkdown(self.spec.get("description_md",""))
        splitter.addWidget(self.desc)

        right = QWidget()
        r = QVBoxLayout(right)

        self.editor = CodeEditor()
        self.editor.setPlainText(self.spec.get("starter_code",""))
        r.addWidget(self.editor)

        btn_row = QHBoxLayout()
        run_btn = QPushButton("Run")
        grade_btn = QPushButton("Submit (Autograde)")
        btn_row.addWidget(run_btn)
        btn_row.addWidget(grade_btn)
        btn_row.addStretch(1)
        r.addLayout(btn_row)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Output / errors appear here…")
        self.output.setFont(QFont("Consolas", 10))
        r.addWidget(self.output)

        splitter.addWidget(right)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)

        root.addWidget(splitter)

        run_btn.clicked.connect(self.on_run)
        grade_btn.clicked.connect(self.on_grade)

        set_last_route("problemsets")

    def on_run(self):
        ok, out = run_code_capture_stdout(self.editor.toPlainText())
        self.output.setPlainText(out if out.strip() else ("✅ Ran with no output." if ok else out))

    def on_grade(self):
        passed, msg = grade_problem(self.editor.toPlainText(), self.spec)
        self.output.setPlainText(msg)
        if passed:
            mark_completed("problemsets", self.problem_id)
            QMessageBox.information(self, "Passed!", "✅ You passed! Next content is unlocked.")
            if callable(self.on_pass):
                self.on_pass()
