from PySide6 import QtWidgets, QtCore, QtGui

from functools import partial

import os
import sys
import json

import maya.mel as mel
import maya.cmds as mc


def getMayaWindow():
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    mayaWin = next(w for w in app.topLevelWidgets() if w.objectName() == 'MayaWindow')

    return mayaWin

def getMenuBar(mainWindow):
    menus = mainWindow.findChildren(QtWidgets.QMenuBar)
    for menu in menus:
        if menu.parent().objectName() == "MayaWindow":
            return menu

def createMenu(mayaMenuFile):
    with open(mayaMenuFile, "r") as mayaJSON:
        mayaMenuData = json.load(mayaJSON)

    mayaWindow = getMayaWindow()
    menuBar = getMenuBar(mayaWindow)

    # Get Menu Name
    menuChildren = mayaMenuData["children"]
    menuName = menuChildren[0]["name"]

    mayaMenu = QtWidgets.QMenu(menuName, parent=mayaWindow)
    mayaMenu.setObjectName(menuName.replace(" ", "_"))
    menuBar.addMenu(mayaMenu)

    # Add refresh option
    refreshAction = mayaMenu.addAction("Refresh Menu")
    refreshAction.triggered.connect(partial(refresh, mayaMenu, mayaMenuFile))
    mayaMenu.addSeparator()

    importTree(mayaMenu, mayaMenuData["children"][0])


def importTree(mayaMenu, menuData):
    def build(item, root):

        for child in root:
            itemName = child["name"]
            action = child["action"]
            icon = child["icon"]
            isMenu = child["isMenu"]
            isSeparator = child["isSeparator"]

            if "language" not in child:
                language = "Python"
            else:
                language = child["language"]

            if not isMenu and not isSeparator:
                optionBoxAction = MayaAction(itemName, action, parent=item)

                optionBoxAction.menuLeft.triggered.connect(partial(runEval, action, language))
                optionBoxAction.menuRight.triggered.connect(partial(addToShelf, itemName, action, icon, language))
                newMenuItem = item.addAction(optionBoxAction)

            elif isMenu:
                newMenuItem = item.addMenu(itemName)
                newMenuItem.setTearOffEnabled(True)
            elif isSeparator:
                newMenuItem = item.addSeparator()

            build(newMenuItem, child["children"])

    root = menuData["children"]
    build(mayaMenu, root)

    return root


def refresh(menu, fileName):
    menuName = menu.objectName()
    menu.setObjectName("deleteMenu")
    createMenu(fileName)
    mc.deleteUI("deleteMenu")


def removeMenu(menuName):
    menuName = menuName.replace(" ", "_")
    mayaWindow = getMayaWindow()
        
    for widget in mayaWindow.children():
        if widget.objectName() == menuName:
            widget.setObjectName("deleteMenu")
            mc.deleteUI("deleteMenu")


def addToShelf(itemName, action, icon, language, *args):
    currentShelfLayout = mel.eval("$tmpVar=$gShelfTopLevel")
    currentShelf = mc.tabLayout(currentShelfLayout, q=True, selectTab=True)

    label = ""
    if not os.path.exists(icon):
        label = itemName
        icon = "pythonFamily.png"

    mc.shelfButton(l=label, i=icon, p=currentShelf, c=action, stp=language.lower(), ann=itemName,
                   style="iconAndTextVertical")
    mel.eval("saveAllShelves $gShelfTopLevel;")
    

def runEval(action, language, *args):
    print(action)

    if language == "MEL":
        mel.eval(action)
    elif language == "Python":
        exec(action)


class OptionBoxAction(QtWidgets.QMenu):
    def __init__(self, parent=None):
        super(OptionBoxAction, self).__init__(parent=parent)

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        action = self.actions()[0]  # should only have one action

        opt = QtWidgets.QStyleOptionMenuItem()
        self.initStyleOption(opt, action)
        opt.text = ''  # only show icon
        opt.icon = QtGui.QIcon(':/checkboxOff.png')
        self.style().drawControl(QtWidgets.QStyle.CE_MenuItem, opt, p, self)


class MayaAction(QtWidgets.QWidgetAction):
    def __init__(self, text, action, parent=None):
        super(MayaAction, self).__init__(parent)

        self.text = text
        self.action = action

        self._widget = QtWidgets.QWidget()
        self.setDefaultWidget(self._widget)

        self.menuLeft = QtWidgets.QMenu(text)
        self.menuLeft.addAction(text)

        self.menuRight = OptionBoxAction()
        self.menuRight.addAction(text)

        self.menuRight.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.menuRight.setFixedSize(QtCore.QSize(20, 20))

        self._widget.setLayout(QtWidgets.QHBoxLayout())
        self._widget.layout().addWidget(self.menuLeft)
        self._widget.layout().addWidget(self.menuRight)
        self._widget.layout().setSpacing(0)
        self._widget.layout().setContentsMargins(0, 0, 0, 0)
