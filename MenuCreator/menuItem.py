from PySide6 import QtWidgets


class MenuItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, itemName, isMenu=False, isSeparator=False):
        super(MenuItem, self).__init__(parent)
        
        self.setText(0, itemName)
        
        self.name = itemName
        self.isMenu = isMenu
        self.isSeparator = isSeparator
        self.icon = ":/pythonFamily.png"
        self.action = ""
        self.language = "MEL"
        self.children = []
    
    def __repr__(self):
        return f"MenuItem(name={self.name}, isMenu={self.isMenu}, isSeparator={self.isSeparator}, icon={self.icon}, action={self.action}, language={self.language}, childCount={len(self.children)})"
    
    def update(self):
        self.setText(0, self.name)
    