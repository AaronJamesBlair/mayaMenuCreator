from PySide6 import QtGui, QtCore
import keyword


class MayaPythonHighlighter(QtGui.QSyntaxHighlighter):
    KEYWORD_EXPRESSION = rf'\bKEYWORD\b'
    STRING_EXPRESSION_DOUBLE = QtCore.QRegularExpression(r'"(?:\\.|[^"\\])*"')
    STRING_EXPRESSION_SINGLE = QtCore.QRegularExpression(r"'(?:\\.|[^'\\])*'")
    COMMENT_EXPRESSION = QtCore.QRegularExpression(r'#.*')

    def __init__(self, parent):
        super().__init__(parent)

        self.highlightingRules = []

        # Format for Python keywords
        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtGui.QColor("#18df00"))
        keywordFormat.setFontWeight(QtGui.QFont.Bold)
        
        if "print" not in keyword.kwlist:
            keyword.kwlist.append("print")
            
        for kw in keyword.kwlist:
            pattern = QtCore.QRegularExpression(self.KEYWORD_EXPRESSION.replace("KEYWORD", kw))
            self.highlightingRules.append((pattern, keywordFormat))

        # String format
        stringFormat = QtGui.QTextCharFormat()
        stringFormat.setForeground(QtGui.QColor("#ffff00"))
        self.highlightingRules.append((self.STRING_EXPRESSION_SINGLE, stringFormat))
        self.highlightingRules.append((self.STRING_EXPRESSION_DOUBLE, stringFormat))

        # Comment format
        commentFormat = QtGui.QTextCharFormat()
        commentFormat.setForeground(QtGui.QColor("#df1825"))
        commentFormat.setFontItalic(True)
        self.highlightingRules.append((self.COMMENT_EXPRESSION, commentFormat))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlightingRules:
            matchIter = pattern.globalMatch(text)
            while matchIter.hasNext():
                match = matchIter.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, fmt)
