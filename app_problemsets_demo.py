# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from src.core.nav import NavigationManager
from src.pages.problem_sets import ProblemSetPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeQuest - PySide6 Desktop")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.nav = NavigationManager(self.stack)

        # DEMO: goes straight to Problem Sets page
        def unlock_next():
            # placeholder: replace with your "hackathon4 unlocked" logic
            print("UNLOCK: hackathon4")

        ps = ProblemSetPage(self.nav, problem_id="ps1_positive_checker", on_pass=unlock_next)
        self.stack.addWidget(ps)
        self.stack.setCurrentWidget(ps)

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.resize(1200, 750)
    w.show()
    app.exec()
