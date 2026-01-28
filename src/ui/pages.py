from __future__ import annotations
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTextEdit, QTextBrowser, QButtonGroup, QRadioButton,
    QMessageBox, QLineEdit, QListWidget, QListWidgetItem, QSplitter, QComboBox
)

from ..engine.grading import grade_quiz, passed
from ..engine.lectures import lecture_for
from ..engine.scaffold import scaffold
from ..engine.runner import run_python

def card():
    f = QFrame()
    f.setObjectName("Card")
    return f

# -------------------- LESSON (W3Schools-style) --------------------
class LessonPage(QWidget):
    def __init__(self, on_next, on_back, on_menu):
        super().__init__()
        self._on_next = on_next
        self._on_back = on_back
        self._on_menu = on_menu
        self._module = {}

        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(12, 12, 12, 12)

        # Top nav (full width)
        nav = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.clicked.connect(self._on_back)
        self.menu_btn = QPushButton("🏠 Menu")
        self.menu_btn.clicked.connect(self._on_menu)

        self.title = QLabel("Lesson")
        self.title.setObjectName("Title")
        self.title.setStyleSheet("font-size:22px;font-weight:900;")

        nav.addWidget(self.back_btn)
        nav.addWidget(self.menu_btn)
        nav.addSpacing(14)
        nav.addWidget(self.title)
        nav.addStretch(1)

        self.next_btn = QPushButton("Take Quiz →")
        self.next_btn.setObjectName("Primary")
        self.next_btn.clicked.connect(self._on_next)
        nav.addWidget(self.next_btn)

        root.addLayout(nav)

        # Splitter: left (toc/examples) | right (content + sandbox)
        split = QSplitter(Qt.Horizontal)
        root.addWidget(split, 1)

        # LEFT PANEL
        left = QFrame()
        left.setObjectName("SidePanel")
        left_l = QVBoxLayout(left)
        left_l.setSpacing(10)

        self.objective = QLabel("")
        self.objective.setWordWrap(True)
        self.objective.setObjectName("Subtle")

        left_l.addWidget(QLabel("Lesson Map"))
        self.toc = QListWidget()
        left_l.addWidget(self.toc, 1)

        left_l.addWidget(QLabel("Examples"))
        self.example_box = QComboBox()
        left_l.addWidget(self.example_box)

        self.load_example_btn = QPushButton("Load Example → Editor")
        self.load_example_btn.clicked.connect(self.load_selected_example)
        left_l.addWidget(self.load_example_btn)

        split.addWidget(left)

        # RIGHT PANEL
        right = QFrame()
        right.setObjectName("MainPanel")
        right_l = QVBoxLayout(right)
        right_l.setSpacing(10)

        self.content = QTextBrowser()
        self.content.setOpenExternalLinks(False)
        self.content.setStyleSheet("font-size:14px;")
        right_l.addWidget(self.content, 3)

        # Sandbox
        sandbox = QFrame()
        sandbox.setObjectName("Card")
        s = QVBoxLayout(sandbox)
        s.setSpacing(8)

        hdr = QHBoxLayout()
        hdr.addWidget(QLabel("Try it (Sandbox)"))
        hdr.addStretch(1)

        self.run_btn = QPushButton("Run ▶")
        self.run_btn.setObjectName("Primary")
        self.run_btn.clicked.connect(self.run_code)
        hdr.addWidget(self.run_btn)

        s.addLayout(hdr)

        self.editor = QTextEdit()
        self.editor.setPlaceholderText("# Load an example or type your code here...")
        self.editor.setMinimumHeight(170)
        s.addWidget(self.editor)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMinimumHeight(120)
        self.output.setPlaceholderText("Output appears here...")
        s.addWidget(self.output)

        right_l.addWidget(sandbox, 2)

        split.addWidget(right)

        # Give more space to right pane
        split.setStretchFactor(0, 1)
        split.setStretchFactor(1, 3)

        # TOC click scrolls content (simple)
        self.toc.itemClicked.connect(self.jump_to_section)

        # Basic nicer look
        self.setStyleSheet(self.styleSheet() + """
        QFrame#SidePanel { border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 10px; }
        QFrame#MainPanel { border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 10px; }
        QTextBrowser { background: rgba(0,0,0,0.15); border-radius: 12px; padding: 12px; }
        """)

    def load_module(self, module: dict):
        self._module = module
        self.title.setText(module.get("title", "Lesson"))
        self.objective.setText(module.get("objective", ""))
        # Build content HTML
        html = module.get("lesson_html", "")
        if not html:
            # fallback to plain text
            txt = module.get("lesson_text", "")
            html = "<pre>" + (txt.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")) + "</pre>"

        self.content.setHtml(html)

        # TOC
        self.toc.clear()
        sections = module.get("sections", [])
        if sections:
            for sec in sections:
                self.toc.addItem(QListWidgetItem(sec))
        else:
            # lightweight default
            for sec in ["Intro", "Key idea", "Examples", "Common mistakes", "Mini practice"]:
                self.toc.addItem(QListWidgetItem(sec))

        # Examples dropdown
        self.example_box.clear()
        self._examples = module.get("examples", [])
        for ex in self._examples:
            self.example_box.addItem(ex.get("title","Example"), ex)

        # Set editor starter scaffold
        starter_task = module.get("starter_task", "Try modifying the example and re-run it.")
        self.editor.setPlainText(scaffold(starter_task))
        self.output.setPlainText("")

    def jump_to_section(self, item: QListWidgetItem):
        # Simple: search for an anchor-like heading text in the HTML and scroll there
        key = item.text().strip()
        self.content.find(key)

    def load_selected_example(self):
        if not hasattr(self, "_examples") or not self._examples:
            return
        ex = self.example_box.currentData()
        if not ex:
            return
        code = ex.get("code","")
        hint = ex.get("task","Try running it, then change one thing.")
        self.editor.setPlainText(scaffold(hint) + "\n" + code)
        self.output.setPlainText("")

    def run_code(self):
        code = self.editor.toPlainText()
        res = run_python(code, timeout_sec=2.0)
        out = ""
        if res.stdout:
            out += res.stdout
        if res.stderr:
            out += ("\n" if out else "") + res.stderr
        if not out:
            out = "(no output)"
        self.output.setPlainText(out)

# -------------------- QUIZ / DEBUG / TERMINAL (unchanged from your last good version) --------------------
class QuizPage(QWidget):
    def __init__(self, on_pass, on_fail, on_back, on_menu):
        super().__init__()
        self._on_pass = on_pass
        self._on_fail = on_fail
        self._on_back = on_back
        self._on_menu = on_menu
        self.quiz = None

        root = QVBoxLayout(self)
        root.setSpacing(14)

        c = card()
        lay = QVBoxLayout(c)
        lay.setSpacing(12)

        nav = QHBoxLayout()
        back = QPushButton("← Back")
        back.clicked.connect(self._on_back)
        menu = QPushButton("🏠 Menu")
        menu.clicked.connect(self._on_menu)
        nav.addWidget(back)
        nav.addWidget(menu)
        nav.addStretch(1)

        title = QLabel("Quiz")
        title.setObjectName("Title")
        sub = QLabel("2 MCQ + 1 FRQ. You must score 90% or higher to pass.")
        sub.setObjectName("Subtle")

        lay.addLayout(nav)
        lay.addWidget(title)
        lay.addWidget(sub)

        self.mcq_blocks = []
        for n in range(2):
            qb = card()
            ql = QVBoxLayout(qb)
            qh = QLabel(f"MCQ {n+1}")
            qh.setStyleSheet("font-weight:800;")
            qtext = QLabel("")
            qtext.setWordWrap(True)

            group = QButtonGroup(self)
            opts = []
            for i in range(4):
                rb = QRadioButton("")
                group.addButton(rb, i)
                opts.append(rb)

            ql.addWidget(qh)
            ql.addWidget(qtext)
            for rb in opts:
                ql.addWidget(rb)

            lay.addWidget(qb)
            self.mcq_blocks.append((qtext, group, opts))

        frqb = card()
        frql = QVBoxLayout(frqb)
        frqh = QLabel("FRQ (syntax error + fix required)")
        frqh.setStyleSheet("font-weight:800;")

        self.frq_prompt = QLabel("")
        self.frq_prompt.setWordWrap(True)

        self.frq_broken = QTextEdit()
        self.frq_broken.setReadOnly(True)

        self.frq_answer = QTextEdit()
        self.frq_answer.setPlaceholderText(
            "# Explain what is wrong\n# Then write the fixed code line(s)\n\n# Your solution here:"
        )

        frql.addWidget(frqh)
        frql.addWidget(self.frq_prompt)
        frql.addWidget(QLabel("Broken code:"))
        frql.addWidget(self.frq_broken)
        frql.addWidget(QLabel("Your answer (must include the fix):"))
        frql.addWidget(self.frq_answer)
        lay.addWidget(frqb)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        self.submit_btn = QPushButton("Submit Quiz")
        self.submit_btn.setObjectName("Primary")
        self.submit_btn.clicked.connect(self.submit)
        btn_row.addWidget(self.submit_btn)
        lay.addLayout(btn_row)

        root.addWidget(c)

    def load_quiz(self, module: dict):
        self.quiz = module.get("quiz", {})
        mcq = self.quiz.get("mcq", [])
        frq = self.quiz.get("frq", {})

        for i in range(2):
            qtext, group, opts = self.mcq_blocks[i]
            item = mcq[i] if i < len(mcq) else {"question":"(missing)", "choices":["A","B","C","D"], "correct_index":0}
            qtext.setText(item.get("question",""))
            choices = item.get("choices", ["A","B","C","D"])
            for j, rb in enumerate(opts):
                rb.setText(choices[j] if j < len(choices) else "")
                rb.setChecked(False)

        self.frq_prompt.setText(frq.get("prompt", "Explain the syntax error and fix it."))
        self.frq_broken.setPlainText(frq.get("broken_code", "print(\"Hello)\n"))
        self.frq_answer.setPlainText(
            "# Explain what is wrong:\n# \n# Fix the code below:\n# \n# Your solution here:\n"
        )

    def submit(self):
        if not self.quiz:
            return
        mcq_picks = []
        for (_, group, _) in self.mcq_blocks:
            mcq_picks.append(group.checkedId())

        answers = {"mcq": mcq_picks, "frq": self.frq_answer.toPlainText()}
        score, detail = grade_quiz(self.quiz, answers)

        if passed(score):
            QMessageBox.information(self, "Passed", f"Score: {score}%\n\nMoving to required Debug Session.")
            self._on_pass(score)
        else:
            if detail.get("frq", {}).get("fix_ok") is False and self.quiz.get("frq", {}).get("expected_fix_contains"):
                QMessageBox.warning(self, "Not Passed", f"Score: {score}%\n\nFRQ must include the corrected code line.\nTry again.")
            else:
                QMessageBox.warning(self, "Not Passed", f"Score: {score}%\n\nYou need 90%+. Review and try again.")
            self._on_fail(score)

class DebugPage(QWidget):
    def __init__(self, on_done, on_back, on_menu):
        super().__init__()
        self._on_done = on_done
        self._on_back = on_back
        self._on_menu = on_menu
        self.items = []
        self.i = 0
        self.understood = set()

        root = QVBoxLayout(self)
        root.setSpacing(14)

        c = card()
        lay = QVBoxLayout(c)
        lay.setSpacing(10)

        nav = QHBoxLayout()
        back = QPushButton("← Back")
        back.clicked.connect(self._on_back)
        menu = QPushButton("🏠 Menu")
        menu.clicked.connect(self._on_menu)
        nav.addWidget(back)
        nav.addWidget(menu)
        nav.addStretch(1)

        self.title = QLabel("Debug Session (Required)")
        self.title.setObjectName("Title")
        self.sub = QLabel("Learn each error in detail. You must complete all 5 to continue.")
        self.sub.setObjectName("Subtle")
        self.progress = QLabel("")
        self.progress.setObjectName("Subtle")

        self.code = QTextEdit()
        self.code.setReadOnly(True)
        self.code.setMinimumHeight(140)

        self.explain = QTextEdit()
        self.explain.setReadOnly(True)
        self.explain.setMinimumHeight(240)

        btns = QHBoxLayout()
        self.mark_btn = QPushButton("Mark understood ✓")
        self.mark_btn.setObjectName("Primary")
        self.mark_btn.clicked.connect(self.mark_understood)

        self.next_btn = QPushButton("Next error →")
        self.next_btn.clicked.connect(self.next_error)

        btns.addWidget(self.mark_btn)
        btns.addWidget(self.next_btn)
        btns.addStretch(1)

        self.done_btn = QPushButton("Go to Hack Terminal → (locked)")
        self.done_btn.setEnabled(False)
        self.done_btn.clicked.connect(self._on_done)

        lay.addLayout(nav)
        lay.addWidget(self.title)
        lay.addWidget(self.sub)
        lay.addWidget(self.progress)
        lay.addWidget(QLabel("Broken code:"))
        lay.addWidget(self.code)
        lay.addWidget(QLabel("Lecture:"))
        lay.addWidget(self.explain)
        lay.addLayout(btns)
        lay.addWidget(self.done_btn)

        root.addWidget(c)

    def load_errors(self, module: dict):
        pack = module.get("error_pack", [])
        self.items = pack[:5]
        while len(self.items) < 5:
            self.items.append({
                "code": "print('Hello)",
                "error": "SyntaxError: unterminated string literal",
                "why": "String quotes must start and end."
            })
        self.i = 0
        self.understood = set()
        self.done_btn.setEnabled(False)
        self.done_btn.setText("Go to Hack Terminal → (locked)")
        self.render()

    def render(self):
        total = len(self.items)
        self.progress.setText(f"Completed: {len(self.understood)}/{total} • Viewing error {self.i+1}/{total}")

        e = self.items[self.i]
        self.code.setPlainText(e.get("code", ""))
        self.explain.setPlainText(lecture_for(e))

        already = self.i in self.understood
        self.mark_btn.setEnabled(not already)
        self.mark_btn.setText("Mark understood ✓" if not already else "Understood ✓")

        if len(self.understood) == total:
            self.done_btn.setEnabled(True)
            self.done_btn.setText("Go to Hack Terminal →")

    def mark_understood(self):
        self.understood.add(self.i)
        self.render()

    def next_error(self):
        if self.i not in self.understood:
            QMessageBox.warning(self, "Locked", "You must click 'Mark understood' before moving on.")
            return
        if self.i < len(self.items) - 1:
            self.i += 1
            self.render()

class TerminalPage(QWidget):
    def __init__(self, get_unlocked, get_objective, on_next_module, on_back, on_menu):
        super().__init__()
        self._get_unlocked = get_unlocked
        self._get_objective = get_objective
        self._on_next_module = on_next_module
        self._on_back = on_back
        self._on_menu = on_menu

        root = QVBoxLayout(self)
        root.setSpacing(14)

        c = card()
        lay = QVBoxLayout(c)
        lay.setSpacing(10)

        nav = QHBoxLayout()
        back = QPushButton("← Back")
        back.clicked.connect(self._on_back)
        menu = QPushButton("🏠 Menu")
        menu.clicked.connect(self._on_menu)
        nav.addWidget(back)
        nav.addWidget(menu)
        nav.addStretch(1)

        title = QLabel("Hack Terminal")
        title.setObjectName("Title")
        self.sub = QLabel("")
        self.sub.setObjectName("Subtle")

        self.term = QTextEdit()
        self.term.setReadOnly(True)
        self.term.setMinimumHeight(360)

        row = QHBoxLayout()
        self.prompt = QLineEdit()
        self.prompt.setPlaceholderText("Type command… (try: help, objective)")
        self.run_btn = QPushButton("Run")
        self.run_btn.setObjectName("Primary")
        self.run_btn.clicked.connect(self.run_command)
        row.addWidget(self.prompt, 1)
        row.addWidget(self.run_btn)

        bottom = QHBoxLayout()
        bottom.addStretch(1)
        self.next_btn = QPushButton("Next Module →")
        self.next_btn.clicked.connect(self._on_next_module)
        bottom.addWidget(self.next_btn)

        lay.addLayout(nav)
        lay.addWidget(title)
        lay.addWidget(self.sub)
        lay.addWidget(self.term)
        lay.addLayout(row)
        lay.addLayout(bottom)

        root.addWidget(c)

        self._write("SYSTEM> booting...\n")
        QTimer.singleShot(300, lambda: self._write("SYSTEM> ready. type 'help'\n"))

    def set_objective_text(self, s: str):
        self.sub.setText(s)

    def _write(self, s: str):
        self.term.moveCursor(QTextCursor.End)
        self.term.insertPlainText(s)
        self.term.ensureCursorVisible()

    def run_command(self):
        cmdline = self.prompt.text().strip()
        if not cmdline:
            return
        self.prompt.setText("")
        self._write(f"> {cmdline}\n")

        unlocked = set(self._get_unlocked())
        cmd = cmdline.split()[0].lower()

        if cmd not in unlocked:
            self._write(f"ERROR> '{cmd}' not unlocked yet.\n")
            self._write("TIP> pass modules to unlock more commands.\n")
            return

        if cmd == "help":
            self._write("Commands unlocked: " + ", ".join(sorted(unlocked)) + "\n")
            self._write("Try: objective, status\n")
        elif cmd == "objective":
            self._write("OBJECTIVE> " + (self._get_objective() or "No objective.") + "\n")
        elif cmd == "status":
            self._write("SYSTEM> Training sim online. Progress saved locally.\n")
        elif cmd == "ls":
            self._write("root/\n  notes.txt\n  training/\n")
        elif cmd == "cat":
            self._write("notes.txt: 'Read specs carefully. Decompose problems. Test small.'\n")
        elif cmd == "cd":
            self._write("SYSTEM> changed directory (simulated).\n")
        elif cmd == "run":
            self._write("SYSTEM> executing (simulated). You will unlock real runs later.\n")
        else:
            self._write("OK\n")