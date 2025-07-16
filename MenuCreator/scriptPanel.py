import maya.cmds as mc
import maya.mel as mel

from PySide6 import QtWidgets, QtGui, QtCore
from MenuCreator import scriptEditor


class ScriptPanel(QtWidgets.QWidget):
    uiInstance = None
        
    def __init__(self):
        super(ScriptPanel, self).__init__()      
        
        self.currentItem = None
        
        self.buildUI()
        self.buildSignals()
    
    def buildUI(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.boldFont = QtGui.QFont()
        self.boldFont.setBold(True)
        
        self.menuItemNameLayout = QtWidgets.QHBoxLayout()
        
        self.menuItemNameLabel = QtWidgets.QLabel("Name: ")
        self.menuItemNameLabel.setFont(self.boldFont)
        self.menuItemField = QtWidgets.QLineEdit()
        
        self.menuItemNameLayout.addWidget(self.menuItemNameLabel)
        self.menuItemNameLayout.addWidget(self.menuItemField)
        
        self.scriptEditor = scriptEditor.CustomScriptEditor()
        
        self.iconLabel = QtWidgets.QLabel("Icon: ")
        self.iconLabel.setFont(self.boldFont)
        
        self.icon = QtWidgets.QPushButton()
        self.icon.setFlat(True)
        
        self.iconImage = QtGui.QIcon(":/mayaIcon.png")
        self.iconSize = self.iconImage.actualSize(self.icon.size())
        
        self.icon.setFixedSize(QtCore.QSize(24, 24))
        self.icon.setIcon(self.iconImage)

        self.scriptEditor.buttonLayout.insertWidget(0, self.iconLabel)
        self.scriptEditor.buttonLayout.insertWidget(1, self.icon)
        
        self.layout.addLayout(self.menuItemNameLayout)
        self.layout.addWidget(self.scriptEditor)
    
    def buildSignals(self):
        self.icon.clicked.connect(self.changeIcon)
        self.menuItemField.editingFinished.connect(self.updateCurrentItemName)
        self.scriptEditor.melButton.toggled.connect(self.updateCurrentItemLanguage)
        self.scriptEditor.textBox.textChanged.connect(self.updateCurrentItemAction)
        
    def changeIcon(self):
        if self.currentItem:
            newIcon = QtWidgets.QFileDialog().getOpenFileName()[0]
            
            if newIcon:
                self.setIcon(newIcon)
    
    def setIcon(self, newIcon):
        self.iconImage = QtGui.QIcon(newIcon)
        self.icon.setIcon(self.iconImage)
        self.icon.setIconSize(self.iconSize)
        self.icon.update()
        
        self.currentItem.icon = newIcon
        
    
    def updateScriptPanel(self, currentItem):
        if currentItem is not None:
            self.currentItem = currentItem
            
            self.scriptEditor.melButton.blockSignals(True)
            
            self.menuItemField.setText(currentItem.name)
            self.scriptEditor.textBox.setText(currentItem.action)
            
            # Update radio button without triggering an update
            if currentItem.language == "MEL":
                self.scriptEditor.melButton.setChecked(True)
            else:
                self.scriptEditor.pythonButton.setChecked(True)
            self.scriptEditor.melButton.blockSignals(False)
    
            # Enable/disable UI elements based on item type
            if currentItem.isMenu or currentItem.isSeparator:
                self.icon.setEnabled(False)
                self.scriptEditor.setEnabled(False)
                
                if currentItem.isSeparator:
                    self.menuItemField.setEnabled(False)
                else:
                    self.menuItemField.setEnabled(True)
                    
            else:
                self.icon.setEnabled(True)
                self.scriptEditor.setEnabled(True)
                self.menuItemField.setEnabled(True)
            
            # Update Icon
            self.iconImage = QtGui.QIcon(currentItem.icon)
            self.icon.setIcon(self.iconImage)
            self.icon.setIconSize(self.iconSize)
            self.icon.update()
              
            # Update Action
            self.scriptEditor.textBox.setText(currentItem.action)
                    
    def updateCurrentItemName(self):
        newName = self.menuItemField.text()
        self.currentItem.name = newName
        self.currentItem.update()
    
    def updateCurrentItemLanguage(self):
        if self.currentItem:
            if self.scriptEditor.melButton.isChecked():
                self.currentItem.language = "MEL"
            else:
                self.currentItem.language = "Python"
    
    def updateCurrentItemAction(self):
        if self.currentItem:
            currentAction = self.scriptEditor.textBox.toPlainText()
            self.currentItem.action = currentAction
    
    def clear(self):
        self.scriptEditor.melButton.setChecked(True)
        self.updateCurrentItemLanguage()
        self.menuItemField.setText("")
        self.setIcon(":/pythonFamily.png")
        self.scriptEditor.textBox.setText("")
        