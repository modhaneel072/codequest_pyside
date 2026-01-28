from PySide6.QtWidgets import QApplication
import sys
from src.ui.main_window import MainWindow

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())