"""
Widget to contain the buttons/control panel for the merge tool. 
"""
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtCore
import gui_config


class controlButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 200, 200)
        self.buttonLayout()



    def buttonLayout(self):
        grid = QGridLayout()
        self.setLayout(grid)

        merge_left_button = QToolButton()
        merge_left_button.setFixedSize(60, 60)
        icon = QtGui.QIcon(gui_config.ICONS["UNDO"])
        merge_left_button.setIcon(icon)
        merge_left_button.setIconSize(QtCore.QSize(25, 25))
        grid.addWidget(merge_left_button, 0, 0)

        merge_right_button = QToolButton()
        merge_right_button.setFixedSize(60, 60)
        icon = QtGui.QIcon(gui_config.ICONS["REDO"])
        merge_right_button.setIcon(icon)
        merge_right_button.setIconSize(QtCore.QSize(25, 25))
        grid.addWidget(merge_right_button, 0, 3)

        next_diff_button = QToolButton()
        next_diff_button.setFixedSize(60, 60)
        icon = QtGui.QIcon(gui_config.ICONS["NEXT_DIFF"])
        next_diff_button.setIcon(icon)
        next_diff_button.setIconSize(QtCore.QSize(25, 25))
        grid.addWidget(next_diff_button, 0, 1)

        prev_diff_button = QToolButton()
        prev_diff_button.setFixedSize(60, 60)
        icon = QtGui.QIcon(gui_config.ICONS["PREV_DIFF"])
        prev_diff_button.setIcon(icon)
        prev_diff_button.setIconSize(QtCore.QSize(25, 25))
        grid.addWidget(prev_diff_button, 0, 2)

