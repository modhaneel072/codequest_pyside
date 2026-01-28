# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from src.core.nav import NavigationManager
from src.pages.boot import BootPage
from src.pages.modules import ModulesPage
from src.pages.lesson import LessonPage
from src.pages.quiz import QuizPage
from src.pages.debug import DebugPage
from src.pages.problem_sets import ProblemSetPage
from src.pages.hackathons import HackathonsPage
from src.core.progress import unlock_next_module, mark_completed, set_last_route

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeQuest")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.nav = NavigationManager(self.stack)

        self.pages = {}

        def show_modules(start_at=None):
            self.pages["modules"].refresh()
            self.nav.go_to(self.pages["modules"])

        def show_lesson(module_id: int):
            lesson = LessonPage(self.nav, module_id=module_id, routes=routes)
            self.stack.addWidget(lesson)
            self.nav.go_to(lesson)

        def show_quiz(quiz_id: str):
            def after_pass():
                mark_completed("quizzes", quiz_id)
                mod = int(quiz_id.split("_")[0].replace("m",""))
                show_debug(debug_id=f"m{mod}_debug")
            q = QuizPage(self.nav, quiz_id=quiz_id, routes=routes, on_pass=after_pass)
            self.stack.addWidget(q)
            self.nav.go_to(q)

        def show_debug(debug_id: str):
            def after_pass():
                mod = int(debug_id.split("_")[0].replace("m",""))
                show_problemset(problem_id=f"m{mod}_ps1", module_id=mod)
            d = DebugPage(self.nav, debug_id=debug_id, routes=routes, on_pass=after_pass)
            self.stack.addWidget(d)
            self.nav.go_to(d)

        def show_problemset(problem_id: str, module_id: int):
            def after_pass():
                unlock_next_module(module_id)
                self.pages["modules"].refresh()
                self.nav.go_to(self.pages["modules"])
            ps = ProblemSetPage(self.nav, problem_id=problem_id, on_pass=after_pass)
            self.stack.addWidget(ps)
            self.nav.go_to(ps)

        def show_hackathons():
            self.pages["hackathons"].refresh()
            self.nav.go_to(self.pages["hackathons"])

        routes = {
            "modules": show_modules,
            "lesson": show_lesson,
            "quiz": show_quiz,
            "debug": show_debug,
            "problemsets": lambda: show_problemset(problem_id="m1_ps1", module_id=1),
            "hackathons": show_hackathons
        }

        self.pages["modules"] = ModulesPage(self.nav, routes)
        self.pages["hackathons"] = HackathonsPage(self.nav)
        self.pages["boot"] = BootPage(self.nav, routes)

        self.nav.set_home(self.pages["boot"])

        self.stack.addWidget(self.pages["boot"])
        self.stack.addWidget(self.pages["modules"])
        self.stack.addWidget(self.pages["hackathons"])

        self.stack.setCurrentWidget(self.pages["boot"])
        set_last_route("boot")

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.resize(1200, 750)
    w.show()
    app.exec()
