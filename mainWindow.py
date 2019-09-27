#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main Window
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import controlButtons
import main_table
import fileIO
import pmEnums


class mainWindow(QMainWindow):    
    def __init__(self, fileA=0, fileB=0):
        super().__init__()        
        self.setWindowTitle("PyMerge")
        self.setGeometry(1000, 1000, 2000, 1000)
        
        layout = QGridLayout()
        
        #add buttons
        layout.addWidget(controlButtons.controlButtons(), 0, 0)

        #load files and generate changesets
        if fileA != 0 and fileB != 0:
            result = fileIO.fileIO().diffFiles(fileA, fileB)
            if result == pmEnums.RESULT.GOOD:
                result = fileIO.fileIO.getChangeSets( changeSetA, changeSetB )

        if result == pmEnums.RESULT.GOOD:
            pass #pass the changesets to window class or whatever to be loaded into the table
        
        #load table
        table_widget = main_table.MainTable()
        layout.addWidget(table_widget, 1, 0)
        table_widget.load_test_files("file1.c", "file2.c")
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)        
        self.initUI()
        
    def initUI(self, fileA=0, fileB=0):
        #start GUI
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
        mergeLeftButton.setShortcut('Ctrl+l')        
        mergeLeftButton.triggered.connect(self.close)
        editMenu.addAction(mergeLeftButton)

        mergeRightButton = QAction("Merge Right", self)
        mergeRightButton.setShortcut('Ctrl+r')        
        mergeRightButton.triggered.connect(self.close)
        editMenu.addAction(mergeRightButton)

        previousDiffButn = QAction("Previous Difference", self)
        previousDiffButn.setShortcut('Ctrl+p')     
        previousDiffButn.triggered.connect(self.close)
        editMenu.addAction(previousDiffButn)
        
        nextDiffButn = QAction("Next Difference", self)
        nextDiffButn.setShortcut('Ctrl+n')   
        nextDiffButn.triggered.connect(self.close)
        editMenu.addAction(nextDiffButn)


def startMain(fileA=0, fileB=0):    
    app = QApplication(sys.argv)
    ex = mainWindow(fileA, fileB)
    sys.exit(app.exec_())
