import sys
import maya.cmds as mc
from PySide6 import QtWidgets, QtGui, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import OpenMayaUI
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


class Window(MayaQWidgetDockableMixin, QtWidgets.QWidget):
        
    WINDOW_TITLE = "Animation Exporter"
    UI_NAME = "AnimationExporter"
    WORKSPACE_NAME = "AnimationExporterWorkspaceControl"
    UI_SCRIPT = "from AnimationExport.AnimationExporter import AnimationExporter\nAnimationExporter().createWorkspaceControl()"
    
    uiInstance = None
        
    def __init__(self):
        super(Window, self).__init__()      

        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.font = QtGui.QFont()
        self.font.setPointSize(10)
        
        self.textBox = QtWidgets.QTextEdit()
        self.textBox.setFont(self.font)
        self.textBox.setTabStopDistance(4 * self.textBox.fontMetrics().horizontalAdvance(' '))

        self.highlighter = MayaPythonHighlighter(self.textBox.document())
        
        self.executeButton = QtWidgets.QPushButton("Execute")
        self.executeButton.clicked.connect(self.executeScript)
        
        self.layout.addWidget(self.textBox)
        self.layout.addWidget(self.executeButton)

        self.textBox.setText("import D9UI from D9Widgets\n\n")
        
    def executeScript(self):
        print(self.textBox.toPlainText())
        exec(self.textBox.toPlainText())

    def restore():
        workspaceControl = OpenMayaUI.MQtUtil.getCurrentParent()
        Window._instance = Window()
        pointer = OpenMayaUI.MQtUtil.findControl(Window._instance.objectName())
        OpenMayaUI.MQtUtil.addWidgetToMayaLayout(
            long(pointer),
            long(workspace_control),
        )


        
def display():
    if Window.uiInstance is None:
        Window.uiInstance = Window()

    Window.uiInstance.show(
        dockable=True,
        uiScript='import Window; Window.restore()',
    )


if __name__ == "__main__":
    display()
