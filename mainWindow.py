#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main Window
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
        
        
        
        


class mainWindow(QMainWindow):    
    def __init__(self, fileA=0, fileB=0):
        super().__init__()
        self.setWindowTitle("PyMerge")

        layout = QGridLayout()

        layout.addWidget(controlButtons(), 0, 0)
        layout.addWidget(controlButtons(), 1, 0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.initUI()
        
    def initUI(self):
        self.menuItems()
        self.show()

    def menuItems(self):
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # MENUBAR
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')

        openFileButton = QAction("Open File", self)
        openFileButton.setShortcut('Ctrl+o')
        openFileButton.triggered.connect(self.close)
        fileMenu.addAction(openFileButton)

        mergeLeftButton = QAction("Merge Left", self)
        #mergeLeftButton.setShortcut()        
        mergeLeftButton.triggered.connect(self.close)
        editMenu.addAction(mergeLeftButton)

        mergeRightButton = QAction("Merge Right", self)
        #mergeRightButton.setShortcut()        
        mergeRightButton.triggered.connect(self.close)
        editMenu.addAction(mergeRightButton)

        previousDiffButn = QAction("Previous Difference", self)
        #previousDiffButn.setShortcut()        
        previousDiffButn.triggered.connect(self.close)
        editMenu.addAction(previousDiffButn)
        
        nextDiffButn = QAction("Next Difference", self)
        #nextDiffButn.setShortcut()        
        nextDiffButn.triggered.connect(self.close)
        editMenu.addAction(nextDiffButn)


def startMain(fileA=0, fileB=0):    
    app = QApplication(sys.argv)
    ex = mainWindow(fileA, fileB)
    sys.exit(app.exec_())
