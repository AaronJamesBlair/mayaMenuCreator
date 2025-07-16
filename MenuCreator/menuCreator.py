import maya.cmds as mc
import maya.mel as mel

from PySide6 import QtWidgets, QtGui, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import OpenMayaUI

from MenuCreator import menuLayout, scriptPanel
from functools import partial

import json
import os


class MenuCreator(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    uiInstance = None
    
    def __init__(self):
        super(MenuCreator, self).__init__()
        self.buildUI()
        self.buildSignals()
    
    def buildUI(self):
        self.setWindowTitle("aMenuCreator")
        
        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        self.fileMenu = self.menuBar.addMenu("File")
        self.newFileAction = self.fileMenu.addAction("Create New Menu")
        self.fileMenu.addSeparator()
        self.openFileAction = self.fileMenu.addAction("Open...")
        self.saveFileAction = self.fileMenu.addAction("Save...")
        
        self.menuPanel = menuLayout.MenuPanel()
        self.scriptPanel = scriptPanel.ScriptPanel()
        
        self.splitter = QtWidgets.QSplitter()
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        
        self.splitter.addWidget(self.menuPanel)
        self.splitter.addWidget(self.scriptPanel)
        
        self.layout.addWidget(self.menuBar)
        self.layout.addWidget(self.splitter)
    
    def buildSignals(self):
        self.menuPanel.menuItemSelected.connect(self.scriptPanel.updateScriptPanel)
        self.newFileAction.triggered.connect(self.createNewMenu)
        self.saveFileAction.triggered.connect(self.saveMenu)
        self.openFileAction.triggered.connect(self.openMenu)
    
    def createNewMenu(self):
        self.menuPanel.clear()
        self.scriptPanel.clear()
        self.menuPanel.addRoot()

    def openMenu(self):
        fileDialog = QtWidgets.QFileDialog()
        openName = fileDialog.getOpenFileName(self, 'Save Custom Maya Menu', '', "MayaMenu (*.mayaMenu)")[0]        
        
        if openName:
            self.setWindowTitle("aMenuCreator - " + os.path.basename(openName))
            self.menuPanel.clear()
            
            with open(openName, "r") as menuJSON:
                menuData = json.load(menuJSON)
                        
            self.menuPanel.importTree(menuData)
    
    def saveMenu(self):
        fileDialog = QtWidgets.QFileDialog()
        saveName = fileDialog.getSaveFileName(self, 'Save Custom Maya Menu', '', "MayaMenu (*.mayaMenu)")[0]
        
        if saveName:           
            treeList = self.exportTree()
                
            with open(saveName, "w") as menuFile:
                menuFile.write(json.dumps(treeList, indent=2))            

    def exportTree(self):
        def build(item, root):
            for row in range(item.childCount()):
                child = item.child(row)
                
                childDict = {}
                
                childDict["name"] = child.name
                childDict["action"] = child.action
                childDict["language"] = child.language
                childDict["icon"] = child.icon
                childDict["isMenu"] = child.isMenu
                childDict["isSeparator"] = child.isSeparator
                childDict["children"] = []

                root["children"].append(childDict)
                
                build(child, childDict)
                
        root = {"children": []}
        build(self.menuPanel.invisibleRootItem(), root)
        
        return root
        
    
def display():
    if MenuCreator.uiInstance is None:
        MenuCreator.uiInstance = MenuCreator()

    MenuCreator.uiInstance.show(dockable=True, uiScript='from MenuCreator import menuCreator; menuCreator.MenuCreator.restore()',)


if __name__ == "__main__":
    display()
