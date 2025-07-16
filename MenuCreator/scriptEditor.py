import maya.cmds as mc
import maya.mel as mel

from PySide6 import QtWidgets, QtGui, QtCore
from MenuCreator import scriptEditorHighlighter


class CustomScriptEditor(QtWidgets.QWidget):
    uiInstance = None
        
    def __init__(self):
        super(CustomScriptEditor, self).__init__()      

        self.layout = QtWidgets.QVBoxLayout(self)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        
        self.font = QtGui.QFont()
        self.font.setPointSize(10)
        
        self.labelFont = QtGui.QFont()
        self.labelFont.setBold(True)
        
        self.languageLabel = QtWidgets.QLabel("Language: ")
        self.languageLabel.setFont(self.labelFont)
        
        self.melButton = QtWidgets.QRadioButton("MEL")
        self.pythonButton = QtWidgets.QRadioButton("Python")
        
        self.melButton.setChecked(True)
        
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.languageLabel)
        self.buttonLayout.addWidget(self.melButton)
        self.buttonLayout.addWidget(self.pythonButton)

        self.textBox = QtWidgets.QTextEdit()
        self.textBox.setFont(self.font)
        self.textBox.setTabStopDistance(4 * self.textBox.fontMetrics().horizontalAdvance(' '))

        self.highlighter = scriptEditorHighlighter.MayaPythonHighlighter(self.textBox.document())
        
        self.executeButton = QtWidgets.QPushButton("Preview")
        self.executeButton.clicked.connect(self.executeScript)
        
        self.layout.addLayout(self.buttonLayout)
        self.layout.addWidget(self.textBox)
        self.layout.addWidget(self.executeButton)
        
    def executeScript(self):
        scriptText = self.textBox.toPlainText()
        if self.pythonButton.isChecked():
            exec(scriptText)
        else:
            mel.eval(scriptText)
    
    def setEnabled(self, state):
        self.executeButton.setEnabled(state)
        self.melButton.setEnabled(state)
        self.pythonButton.setEnabled(state)
        self.textBox.setEnabled(state)
