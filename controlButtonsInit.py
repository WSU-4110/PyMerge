"""
Widget to contain the buttons/control panel for the merge tool.
"""
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore
import gui_config


class controlButtons(QWidget):
    def __init__(self, tableObj):
        super().__init__()
        self.setGeometry(200, 200, 200, 200)
        self.buttonLayout(tableObj)

    def buttonLayout(self, tableObj):
        grid = QGridLayout()
        self.setLayout(grid)
        print(id(tableObj))

        merge_left_button = QToolButton()
        merge_left_button.setFixedSize(80, 50)
        icon = QtGui.QIcon(gui_config.ICONS["MERGE_LEFT"])
        merge_left_button.setIcon(icon)
        merge_left_button.clicked.connect(tableObj.merge_left)
        grid.addWidget(merge_left_button, 0, 0)


