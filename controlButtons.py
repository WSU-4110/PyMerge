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
        merge_left_button.setFixedSize( 80, 50)
        icon = QtGui.QIcon(gui_config.ICONS["MERGE_LEFT"])
        merge_left_button.setIcon(icon)
        merge_left_button.clicked.connect(tableObj.merge_left)
        grid.addWidget(merge_left_button, 0, 0)


        undo_change_button = QToolButton()
        undo_change_button.setFixedSize( 80, 50)
        icon = QtGui.QIcon(gui_config.ICONS["UNDO"])
        undo_change_button.setIcon(icon)
        # undo_change_button.clicked.connect(tableObj.undo_last_change)
        undo_change_button.clicked.connect(tableObj.undo_last_change)
        grid.addWidget(undo_change_button, 0, 1)
        
        next_diff_button = QToolButton()
        next_diff_button.setFixedSize( 80, 50)
        icon = QtGui.QIcon(gui_config.ICONS["NEXT_DIFF"])
        next_diff_button.setIcon(icon)
        next_diff_button.clicked.connect(tableObj.write_merged_files)
        grid.addWidget(next_diff_button, 1, 2)
        
        prev_diff_button = QToolButton()
        prev_diff_button.setFixedSize( 80, 50)
        icon = QtGui.QIcon(gui_config.ICONS["PREV_DIFF"])
        prev_diff_button.setIcon(icon)
        prev_diff_button.clicked.connect(tableObj.goto_prev_diff)
        grid.addWidget(prev_diff_button, 0, 2)

        redo_change_button = QToolButton()
        redo_change_button.setFixedSize( 80, 50)
        icon = QtGui.QIcon(gui_config.ICONS["REDO"])
        redo_change_button.setIcon(icon)
        redo_change_button.clicked.connect(tableObj.redo_last_undo)
        grid.addWidget(redo_change_button, 0, 3)

        
        merge_right_button = QToolButton()
        merge_right_button.setFixedSize( 80, 50)
        icon = QtGui.QIcon(gui_config.ICONS["MERGE_RIGHT"])
        merge_right_button.setIcon(icon)
        merge_right_button.clicked.connect(tableObj.merge_right)
        grid.addWidget(merge_right_button, 0, 4)
