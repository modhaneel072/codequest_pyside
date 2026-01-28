from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtWidgets import QWidget

def slide_in(widget: QWidget, from_right: bool = True, duration_ms: int = 240):
    end_pos = widget.pos()
    start_pos = QPoint(end_pos.x() + (40 if from_right else -40), end_pos.y())
    widget.move(start_pos)
    anim = QPropertyAnimation(widget, b"pos", widget)
    anim.setStartValue(start_pos)
    anim.setEndValue(end_pos)
    anim.setDuration(duration_ms)
    anim.setEasingCurve(QEasingCurve.OutCubic)
    anim.start()
    widget._anim = anim