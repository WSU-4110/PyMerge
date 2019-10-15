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
import diff_resolution
import fileOpenDialog


class mainWindow(QMainWindow):    
    def __init__(self, fileA=0, fileB=0):
        super().__init__()        
        self.setWindowTitle("PyMerge")
        self.setGeometry(1000, 1000, 2000, 1000)        
        layout = QGridLayout()

        #load files and generate changesets
        result = pmEnums.RESULT.ERROR
        fIO = fileIO.fileIO()
        if fileA != 0 and fileB != 0:            
            result = fIO.diffFiles(fileA, fileB)
            if result == pmEnums.RESULT.GOOD:
                result = fIO.getChangeSets(fIO.changesA, fIO.changesB)
            
        
        if result == pmEnums.RESULT.GOOD:
            pass #pass the changesets to window class or whatever to be loaded into the table

    
        table_widget = 0
        if( fileA != 0 and fileB != 0 ):
            #load table
            table_widget = main_table.MainTable(fIO.changesA, fIO.changesB)            
            #add table
            layout.addWidget(table_widget, 1, 0)
            #table_widget.load_test_files("file1.c", "file2.c")
            table_widget.load_table_contents([], [], fileA, fileB)    # Left list arguments for now            
        else:   
            #load empty table
            table_widget = main_table.MainTable(fIO.changesA, fIO.changesB)            
            #add table
            layout.addWidget(table_widget, 1, 0)
            #table_widget.load_test_files("file1.c", "file2.c")
            table_widget.load_table_contents([], [])    # Left list arguments for now
            
        print(id(table_widget))
        layout.addWidget(controlButtons.controlButtons(table_widget), 0, 0)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)                
        self.initUI(table_widget)
    
        
    def initUI(self, tableObj=0):
        #start GUI
        if(tableObj):
            self.menuItems(tableObj)        
        self.show()

    def openFile(self, tableObj):
        fileOpener = fileOpenDialog.fileOpenDialog()
        #fileA = fileOpener.fileAName
        #fileB = fileOpener.fileBName
        fileA = "file1.c"
        fileB = "file2.c"
        tableObj.load_table_contents([], [], fileA, fileB)
        
        
    def menuItems(self, tableObj):
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # MENUBAR
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')

        
        
        openFileButton = QAction("Open File", self)
        openFileButton.setShortcut('Ctrl+o')
        openFileButton.triggered.connect(lambda:self.openFile(tableObj))
        fileMenu.addAction(openFileButton)

        mergeLeftButton = QAction("Merge Left", self)
        mergeLeftButton.setShortcut('Ctrl+l')        
        #mergeLeftButton.triggered.connect(tableObj.mergeLeft)
        editMenu.addAction(mergeLeftButton)

        mergeRightButton = QAction("Merge Right", self)
        mergeRightButton.setShortcut('Ctrl+r')        
        #mergeRightButton.triggered.connect(tableObj.mergeRight)
        editMenu.addAction(mergeRightButton)

        previousDiffButn = QAction("Previous Difference", self)
        previousDiffButn.setShortcut('Ctrl+p')     
        previousDiffButn.triggered.connect(tableObj.goto_prev_diff)
        editMenu.addAction(previousDiffButn)
        
        nextDiffButn = QAction("Next Difference", self)
        nextDiffButn.setShortcut('Ctrl+n')   
        nextDiffButn.triggered.connect(tableObj.goto_next_diff)
        editMenu.addAction(nextDiffButn)

        undoChangeButn = QAction("Undo", self)
        undoChangeButn.setShortcut('Ctrl+z')   
        undoChangeButn.triggered.connect(tableObj.undo_last_change)
        editMenu.addAction(undoChangeButn)

        redoChangeButn = QAction("Redo", self)
        redoChangeButn.setShortcut('Ctrl+y')   
        redoChangeButn.triggered.connect(tableObj.redo_last_undo)
        editMenu.addAction(redoChangeButn)

        
#

def startMain(fileA=0, fileB=0):    
    app = QApplication(sys.argv)
    ex = mainWindow(fileA, fileB)
    sys.exit(app.exec_())
