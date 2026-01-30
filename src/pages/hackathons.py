# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from src.core.progress import hackathons_unlocked, set_last_route

class HackathonsPage(QWidget):
    def __init__(self, nav):
        super().__init__()
        self.nav = nav
        root = QVBoxLayout(self)

        top = QHBoxLayout()
        back = QPushButton("Back")
        back.clicked.connect(self.nav.go_back)
        title = QLabel("Hackathons")
        title.setStyleSheet("font-size:18px; font-weight:800;")
        top.addWidget(back); top.addStretch(1); top.addWidget(title); top.addStretch(1)
        root.addLayout(top)

        self.status = QLabel("")
        root.addWidget(self.status)

        start = QPushButton("Start Hackathon (if unlocked)")
        start.setMinimumHeight(44)
        start.clicked.connect(self.try_start)
        root.addWidget(start)

        set_last_route("hackathons")
        self.refresh()

    def refresh(self):
        if hackathons_unlocked():
            self.status.setText("✅ Hackathons unlocked! Pick one and begin.")
        else:
            self.status.setText("🔒 Hackathons locked. Finish more modules to unlock.")

    def try_start(self):
        if not hackathons_unlocked():
            QMessageBox.warning(self, "Locked", "Hackathons unlock after you finish more modules.")
        else:
            QMessageBox.information(self, "Soon", "Hackathon missions will go here next.")
