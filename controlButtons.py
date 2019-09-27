"""
Widget to contain the buttons/control panel for the merge tool. 
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import os.path
sys.path.append('icons/')
import iconStrings


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
        icon = QtGui.QIcon( os.path.join( "icons/", iconStrings.MERGERICON ))
        mergeLBut.setIcon(icon)
        
        grid.addWidget(mergeLBut, 0, 0)

        mergeRBut = QPushButton()
        icon = QtGui.QIcon( os.path.join( "icons/", iconStrings.MERGELICON ))
        mergeRBut.setIcon(icon)
        grid.addWidget(mergeRBut, 0, 2)
        
        nextDBut =  QPushButton()
        icon = QtGui.QIcon( os.path.join( "icons/", iconStrings.NEXTDIFFICON ))
        nextDBut.setIcon(icon)
        grid.addWidget(nextDBut, 0, 1)
        
        prevDBut =  QPushButton()
        icon = QtGui.QIcon( os.path.join( "icons/", iconStrings.PREVDIFFICON ))
        prevDBut.setIcon(icon)
        grid.addWidget(prevDBut, 1, 1)
        
