# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextBrowser, QSplitter, QMessageBox, QPlainTextEdit
from PySide6.QtCore import Qt
from src.core.io import load_json
from src.core.debug import run_debug
from src.core.progress import mark_completed, set_last_route
from src.widgets.code_editor import CodeEditor

class DebugPage(QWidget):
    def __init__(self, nav, debug_id: str, routes, on_pass=None):
        super().__init__()
        self.nav = nav
        self.routes = routes
        self.on_pass = on_pass
        self.spec = load_json(f"src/data/debugs/{debug_id}.json")
        self.debug_id = debug_id

        root = QVBoxLayout(self)
        top = QHBoxLayout()

        back = QPushButton("← Back")
        back.clicked.connect(self.nav.go_back)
        title = QLabel(self.spec.get("title", "Debug Mission"))
        title.setStyleSheet("font-size:18px; font-weight:800;")

        top.addWidget(back); top.addStretch(1); top.addWidget(title); top.addStretch(1)
        root.addLayout(top)

        splitter = QSplitter(Qt.Horizontal)

        left = QTextBrowser()
        left.setMarkdown(self.spec.get("description_md", "Fix the code."))
        splitter.addWidget(left)

        right = QWidget()
        r = QVBoxLayout(right)

        self.editor = CodeEditor()
        self.editor.setPlainText(self.spec.get("broken_code", ""))
        r.addWidget(self.editor)

        btns = QHBoxLayout()
        run_btn = QPushButton("Run / Check")
        btns.addWidget(run_btn)
        btns.addStretch(1)
        r.addLayout(btns)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Autograder output…")
        r.addWidget(self.output)

        splitter.addWidget(right)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        root.addWidget(splitter)

        run_btn.clicked.connect(self.check)

        set_last_route("modules")

    def check(self):
        passed, msg = run_debug(self.spec, self.editor.toPlainText())
        self.output.setPlainText(msg)
        if passed:
            mark_completed("debugs", self.debug_id)
            QMessageBox.information(self, "Passed", "✅ Debug mission passed! Next unlocked.")
            if callable(self.on_pass):
                self.on_pass()
