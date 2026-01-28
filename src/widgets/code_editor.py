# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QTextFormat, QFont, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtWidgets import QPlainTextEdit, QWidget

# ---- Syntax highlighter (simple, good enough to feel like an editor)
class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, doc):
        super().__init__(doc)
        self.rules = []

        def fmt(bold=False, italic=False):
            f = QTextCharFormat()
            if bold: f.setFontWeight(QFont.Weight.Bold)
            if italic: f.setFontItalic(True)
            return f

        kw = fmt(bold=True)
        self.keyword_patterns = [
            r"\bdef\b", r"\breturn\b", r"\bif\b", r"\belif\b", r"\belse\b",
            r"\bfor\b", r"\bwhile\b", r"\bbreak\b", r"\bcontinue\b",
            r"\bTrue\b", r"\bFalse\b", r"\bNone\b", r"\bimport\b", r"\bfrom\b",
            r"\bprint\b", r"\binput\b", r"\bint\b", r"\bfloat\b", r"\bstr\b", r"\blen\b"
        ]
        self.rules += [(p, kw) for p in self.keyword_patterns]

        self.string_fmt = fmt()
        self.comment_fmt = fmt(italic=True)

    def highlightBlock(self, text: str):
        import re
        # strings
        for m in re.finditer(r"('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")", text):
            self.setFormat(m.start(), m.end()-m.start(), self.string_fmt)
        # comments
        c = text.find("#")
        if c != -1:
            self.setFormat(c, len(text)-c, self.comment_fmt)
        # keywords
        for p, f in self.rules:
            for m in __import__("re").finditer(p, text):
                self.setFormat(m.start(), m.end()-m.start(), f)

# ---- Line-number area
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Consolas", 11))
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(' '))
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

        self.highlighter = PythonHighlighter(self.document())

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(20, 20, 20))  # dark gutter

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QColor(140, 140, 140))
                painter.drawText(0, top, self.lineNumberArea.width()-4, self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def highlight_current_line(self):
        extra = []
        sel = self.ExtraSelection()
        sel.format.setBackground(QColor(35, 35, 35))
        sel.format.setProperty(QTextFormat.FullWidthSelection, True)
        sel.cursor = self.textCursor()
        sel.cursor.clearSelection()
        extra.append(sel)
        self.setExtraSelections(extra)

    def keyPressEvent(self, e):
        # Make Tab insert spaces
        if e.key() == Qt.Key_Tab:
            self.insertPlainText(" " * 4)
            return
        super().keyPressEvent(e)
