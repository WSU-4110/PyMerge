"""
Widget to contain the buttons/control panel for the merge tool. 
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
#from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QGridLayout, QPushButton, QGroupBox, QDialog, QVBoxLayout



class controlButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 200, 200)
        self.buttonLayout()
                
    def buttonLayout(self):        
        grid = QGridLayout()
        self.setLayout(grid)
        
        mergeLBut = QPushButton("Merge Left")
        grid.addWidget(mergeLBut, 0, 0)
        mergeRBut = QPushButton("Merge Right")
        grid.addWidget(mergeRBut, 0, 3)
        nextDBut =  QPushButton("Next Difference")
        grid.addWidget(nextDBut, 0, 1)
        prevDBut =  QPushButton("Previous Difference")
        grid.addWidget(prevDBut, 0, 2)
        
