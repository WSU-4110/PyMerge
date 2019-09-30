"""
Widget to contain the buttons/control panel for the merge tool. 
"""

import sys
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
                
        mergeLBut = QPushButton()
        mergeLBut.resize( 100, 40)        
        icon = QtGui.QIcon( gui_config.ICONS['MERGE_LEFT'] )
        mergeLBut.setIcon(icon)
        
        grid.addWidget(mergeLBut, 0, 0)

        mergeRBut = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS['MERGE_RIGHT'] )
        mergeRBut.setIcon(icon)
        grid.addWidget(mergeRBut, 0, 2)
        
        nextDBut =  QPushButton()
        icon = QtGui.QIcon( gui_config.ICONS['NEXT_DIFF'])
        nextDBut.setIcon(icon)
        grid.addWidget(nextDBut, 1, 1)
        
        prevDBut =  QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS['PREV_DIFF'])
        prevDBut.setIcon(icon)
        grid.addWidget(prevDBut, 0, 1)
        
