"""
Widget to contain the buttons/control panel for the merge tool. 
"""
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

import gui_config


class controlButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 200, 200)
        self.buttonLayout()
                
    def buttonLayout(self):        
        grid = QGridLayout()
        self.setLayout(grid)
                

        merge_left_button = QPushButton()
        merge_left_button.resize( 100, 40)
        icon = QtGui.QIcon(gui_config.ICONS["MERGE_LEFT"])
        merge_left_button.setIcon(icon)
        
        grid.addWidget(merge_left_button, 0, 0)


        merge_right_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["MERGE_RIGHT"])
        merge_right_button.setIcon(icon)
        grid.addWidget(merge_right_button, 0, 2)
        
        next_diff_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["NEXT_DIFF"])
        next_diff_button.setIcon(icon)
        grid.addWidget(next_diff_button, 0, 1)
        
        prev_diff_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["PREV_DIFF"])
        prev_diff_button.setIcon(icon)
        grid.addWidget(prev_diff_button, 1, 1)

        
