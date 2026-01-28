# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from src.core.progress import load_progress, set_last_route

class BootPage(QWidget):
    def __init__(self, nav, routes):
        super().__init__()
        self.nav = nav
        self.routes = routes

        root = QVBoxLayout(self)

        title = QLabel("CodeQuest")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: 900;")

        tagline = QLabel("Learn Python slowly. Unlock missions as you progress.")
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet("opacity: 0.85;")

        root.addSpacing(10)
        root.addWidget(title)
        root.addWidget(tagline)
        root.addSpacing(20)

        btns = QVBoxLayout()

        continue_btn = QPushButton("Continue")
        start_btn = QPushButton("Start Course")
        modules_btn = QPushButton("Modules")
        ps_btn = QPushButton("Problem Sets")
        hacks_btn = QPushButton("Hackathons")

        for b in [continue_btn, start_btn, modules_btn, ps_btn, hacks_btn]:
            b.setMinimumHeight(44)
            btns.addWidget(b)

        root.addLayout(btns)

        continue_btn.clicked.connect(self.on_continue)
        start_btn.clicked.connect(lambda: self.routes["modules"](start_at=1))
        modules_btn.clicked.connect(lambda: self.routes["modules"]())
        ps_btn.clicked.connect(lambda: self.routes["problemsets"]())
        hacks_btn.clicked.connect(lambda: self.routes["hackathons"]())

        footer = QHBoxLayout()
        footer.addStretch(1)
        hint = QLabel("Tip: Continue resumes where you left off.")
        hint.setStyleSheet("opacity: 0.7;")
        footer.addWidget(hint)
        footer.addStretch(1)
        root.addLayout(footer)

        set_last_route("boot")

    def on_continue(self):
        p = load_progress()
        r = p.get("last_route", "boot")
        if r == "problemsets":
            self.routes["problemsets"]()
        elif r == "hackathons":
            self.routes["hackathons"]()
        else:
            self.routes["modules"]()
