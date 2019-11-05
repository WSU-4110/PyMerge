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


