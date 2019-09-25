#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main Window
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import controlButtons

class mainWindow(QMainWindow):    
    def __init__(self, fileA=0, fileB=0):
        super().__init__()
        self.setWindowTitle("PyMerge")

        layout = QGridLayout()

        layout.addWidget(controlButtons.controlButtons(), 0, 0)
        layout.addWidget(controlButtons.controlButtons(), 1, 0)

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
