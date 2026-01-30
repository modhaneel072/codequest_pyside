from __future__ import annotations
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QApplication

from .boot_menu import BootMenu
from .pages import LessonPage, QuizPage, DebugPage, ChallengePage, TerminalPage
from .pages import LessonPage, QuizPage, DebugPage, ChallengePage, TerminalPage
from ..engine.content_loader import load_course, load_progress, save_progress
from ..engine.progress import record_attempt, unlock_after_pass
from ..ui.styles import APP_QSS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeQuest - PySide6 Desktop")
        self.resize(1200, 760)

        self.course = load_course()
        self.progress = load_progress()

        self.stack = QStackedWidget()

        # Boot menu
        self.boot = BootMenu(
            start_course=self.go_lesson,
            review=self.go_lesson,
            progress=self.show_progress,
            hack_progress=self.go_terminal,
            settings=self.show_settings,
            exit_app=QApplication.quit
        )

        # Pages (now include back/menu)
        self.lesson_page = LessonPage(on_next=self.go_quiz, on_back=self.go_menu, on_menu=self.go_menu)
        self.quiz_page = QuizPage(on_pass=self.quiz_pass, on_fail=self.quiz_fail, on_back=self.go_lesson, on_menu=self.go_menu)
        self.debug_page = DebugPage(on_done=self.show_challenge, on_back=self.go_quiz, on_menu=self.go_menu)
        self.challenge_page = ChallengePage(on_pass=self.on_challenge_pass, on_back=self.go_back, on_menu=self.go_menu)
        self.terminal_page = TerminalPage(get_unlocked=self.get_unlocked_cmds, get_objective=self.get_hack_prompt,
            on_next_module=self.next_module, on_back=self.go_menu, on_menu=self.go_menu)

        self.stack.addWidget(self.boot)          # 0
        self.stack.addWidget(self.lesson_page)   # 1
        self.stack.addWidget(self.quiz_page)     # 2
        self.stack.addWidget(self.debug_page)
        self.stack.addWidget(self.challenge_page)    # 3
        self.stack.addWidget(self.terminal_page) # 4

        root = QWidget()
        lay = QVBoxLayout(root)
        lay.addWidget(self.stack)
        self.setCentralWidget(root)

        self.setStyleSheet(APP_QSS)
        self.stack.setCurrentWidget(self.boot)

    def modules(self):
        return self.course.get("modules", [])

    def current_module_index(self) -> int:
        return int(self.progress.get("module_index", 0))

    def current_module(self) -> dict:
        mods = self.modules()
        if not mods:
            return {}
        i = self.current_module_index()
        if i < 0: i = 0
        if i >= len(mods): i = len(mods) - 1
        return mods[i]

    def load_current_module(self):
        mod = self.current_module()
        self.lesson_page.load_module(mod)
        self.quiz_page.load_quiz(mod)
        self.debug_page.load_errors(mod)
        self.terminal_page.set_objective_text(self.get_hack_prompt())

    # NAV
    def go_menu(self):
        self.stack.setCurrentWidget(self.boot)

    def go_back(self):
        """Context-aware back button so users can't bypass gates."""
        current = self.stack.currentWidget()

        # Challenge back -> Debug
        if hasattr(self, "challenge_page") and current is self.challenge_page:
            self.stack.setCurrentWidget(self.debug_page)
            return

        # Debug back -> Quiz
        if current is self.debug_page:
            self.stack.setCurrentWidget(self.quiz_page)
            return

        # Quiz back -> Lesson
        if current is self.quiz_page:
            self.stack.setCurrentWidget(self.lesson_page)
            return

        # Default -> Menu
        self.go_menu()

    def go_lesson(self):
        self.load_current_module()
        self.stack.setCurrentWidget(self.lesson_page)

    def go_quiz(self):
        self.stack.setCurrentWidget(self.quiz_page)

    def quiz_pass(self, score: int):
        mi = self.current_module_index()
        record_attempt(self.progress, mi, score)
        unlock_after_pass(self.progress, mi)
        save_progress(self.progress)

        # FORCE debug after passing
        self.load_current_module()
        self.stack.setCurrentWidget(self.debug_page)

    def quiz_fail(self, score: int):
        mi = self.current_module_index()
        record_attempt(self.progress, mi, score)
        save_progress(self.progress)
        self.go_lesson()

    def go_terminal(self):
        self.terminal_page.set_objective_text(self.get_hack_prompt())
        self.stack.setCurrentWidget(self.terminal_page)

    def next_module(self):
        # After terminal, allow moving forward
        if self.current_module_index() >= len(self.modules()):
            self.go_menu()
            return
        self.go_lesson()

    # TODO: MENU and other menu handlers still need to be implemented
    def show_progress(self):
        self.go_lesson()

    def show_settings(self):
        self.go_menu()

    def get_unlocked_cmds(self):
        return self.progress.get("terminal_unlocked", {}).get("commands", ["help", "objective", "status"])

    def get_hack_prompt(self) -> str:
        return self.current_module().get("hack_prompt", "No objective set.")

# ---- Challenge flow hooks ----

    def show_challenge(self):
        # called after debug session
        module = self.current_module()
        self.challenge_page.load_challenge(module)
        self.stack.setCurrentWidget(self.challenge_page)

    def on_challenge_pass(self):
        # only after passing coding challenge can they go to hack terminal
        self.show_terminal()