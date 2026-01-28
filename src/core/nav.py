# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QStackedWidget

class NavigationManager:
    def __init__(self, stack: QStackedWidget):
        self.stack = stack
        self.history: list[int] = []
        self.home_widget = None

    def set_home(self, widget):
        self.home_widget = widget

    def go_to(self, widget):
        self.history.append(self.stack.currentIndex())
        self.stack.setCurrentWidget(widget)

    def go_back(self):
        if self.history:
            self.stack.setCurrentIndex(self.history.pop())
        elif self.home_widget is not None:
            self.stack.setCurrentWidget(self.home_widget)
