# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem
from src.core.progress import load_progress, set_last_route

class ModulesPage(QWidget):
    def __init__(self, nav, routes):
        super().__init__()
        self.nav = nav
        self.routes = routes

        root = QVBoxLayout(self)
        top = QHBoxLayout()

        back = QPushButton("Back")
        back.clicked.connect(self.nav.go_back)

        title = QLabel("Modules (W3Schools pace)")
        title.setStyleSheet("font-size: 18px; font-weight: 800;")

        top.addWidget(back); top.addStretch(1); top.addWidget(title); top.addStretch(1)
        root.addLayout(top)

        self.list = QListWidget()
        root.addWidget(self.list)
        self.refresh()
        self.list.itemClicked.connect(self.open_module)

        set_last_route("modules")

    def refresh(self):
        self.list.clear()
        p = load_progress()
        unlocked = p.get("unlocked_module", 1)

        for i in range(1, 6):
            it = QListWidgetItem(f"Module {i}")
            if i > unlocked:
                it.setText(f"Module {i}  🔒 Locked")
                it.setFlags(it.flags() & ~it.flags().__class__.ItemIsEnabled)
            self.list.addItem(it)

    def open_module(self, item):
        mod = int(item.text().split()[1])
        self.routes["lesson"](module_id=mod)
