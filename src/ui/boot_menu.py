from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class BootMenu(QWidget):
    def __init__(self, start_course, review, progress, hack_progress, settings, exit_app):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setSpacing(18)

        title = QLabel("CODEQUEST")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:28px;font-weight:900;")

        def btn(text, fn):
            b = QPushButton(text)
            b.setMinimumHeight(46)
            b.clicked.connect(fn)
            return b

        lay.addStretch()
        lay.addWidget(title)
        lay.addStretch()

        lay.addWidget(btn("Start / Continue Course", start_course))
        lay.addWidget(btn("Review Lessons", review))
        lay.addWidget(btn("Course Progress", progress))
        lay.addWidget(btn("Hackathon Progress", hack_progress))
        lay.addWidget(btn("Settings", settings))
        lay.addWidget(btn("Exit", exit_app))

        lay.addStretch()