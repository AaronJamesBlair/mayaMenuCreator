import maya.cmds as mc
import maya.mel as mel

from PySide6 import QtWidgets, QtGui, QtCore
from MenuCreator import menuItem
from functools import partial


class MenuPanel(QtWidgets.QTreeWidget):
    menuItemSelected = QtCore.Signal(object)
    
    def __init__(self):
        super(MenuPanel, self).__init__()
        self.header().hide()
                
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuRequested)
        
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        
        self.currentItemChanged.connect(self.updateAttributePanel)
        
        self.addRoot()
        
    def addRoot(self):
        self.addItem("Menu Name", isMenu=True)
        
    def addItem(self, itemName, isMenu=False, isSeparator=False):
        currentItem = self.currentItem()
                
        if not currentItem:
            currentItem = self
        
        newItem = menuItem.MenuItem(currentItem, itemName, isMenu=isMenu, isSeparator=isSeparator)
        
        self.clearSelection()
        newItem.setSelected(True)
        self.menuItemSelected.emit(newItem)
        
        return newItem
        
    def contextMenuRequested(self, position):
        currentItem = self.currentItem()
        
        if currentItem:
            menu = QtWidgets.QMenu()
            
            self.addItemAction = menu.addAction("Add Item")
            self.addSubMenuAction = menu.addAction("Add SubMenu")

            self.addSeparatorAction = menu.addAction("Add Separator")
            menu.addSeparator()
            
            self.removeItemAction = menu.addAction("Remove Item")
            self.removeItemAction.triggered.connect(self.removeItem)
            
            self.addItemAction.triggered.connect(partial(self.addItem, "menuItem"))
            self.addSubMenuAction.triggered.connect(partial(self.addItem, "menu", isMenu=True))
            self.addSeparatorAction.triggered.connect(partial(self.addItem, "---------------------------------------------", isSeparator=True))
            
            action = menu.exec(self.mapToGlobal(QtCore.QPoint(position.x(), position.y())))

    def updateAttributePanel(self):
        currentItem = self.currentItem()
        self.menuItemSelected.emit(currentItem)
    
    def removeItem(self):
        currentItem = self.currentItem()
        currentItem.parent().removeChild(currentItem)
    
    def importTree(self, menuData):
        def build(item, root):
            for child in root:
                itemName = child["name"]   
                                                        
                newItem = menuItem.MenuItem(item, itemName)
                newItem.name = child["name"]
                newItem.action = child["action"]
                newItem.language = child["language"]
                newItem.icon = child["icon"]
                newItem.isMenu = child["isMenu"]
                newItem.isSeparator = child["isSeparator"]
                                
                build(newItem, child["children"])
                
        root = menuData["children"]
        build(self.invisibleRootItem(), root)
        
        return root
