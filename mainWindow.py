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
import os.path
import utilities


class mainWindow(QMainWindow, QMessageBox):
    def __init__(self, fileA=0, fileB=0):
        super().__init__()
        self.setWindowTitle("PyMerge")
        self.setGeometry(1000, 1000, 2000, 1000)
        layout = QGridLayout()

        # load files and generate changesets
        result = pmEnums.RESULT.ERROR
        self.fIO = fileIO.fileIO()
        if fileA != 0 and fileB != 0:
            result = self.fIO.diffFiles(fileA, fileB)
            if result == pmEnums.RESULT.GOOD:
                result = self.fIO.getChangeSets(self.fIO.changesA, self.fIO.changesB)
                
        if result == pmEnums.RESULT.GOOD:
            pass #pass the changesets to window class or whatever to be loaded into the table

        table_widget = 0   
        #load table
        table_widget = main_table.MainTable(self.fIO.changesA, self.fIO.changesB)            
        #add table

        layout.addWidget(table_widget, 1, 0)

        #load table with fileA and B if present from command line
        if fileA != 0 and fileB != 0:
            table_widget.load_table_contents(fileA, fileB)  # Left list arguments for now
        table_widget.load_table_contents()  # Left list arguments for now
        
        control_buttons_widget = controlButtons.controlButtons(table_widget)
        layout.addWidget(control_buttons_widget, 0, 0)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.initUI(table_widget, control_buttons_widget)

    def initUI(self, tableObj=0, butn_widget=0):
        # start GUI
        if tableObj:
            self.menuItems(tableObj, butn_widget)
        self.show()

    def openFile(self, tableObj):

        tableObj.clear_table()
        
        fileOpener = fileOpenDialog.fileOpenDialog()

        fileA = fileOpener.fileAName
        fileB = fileOpener.fileBName

        if not os.path.exists(fileA):
            print(fileA, "Does not exist")
        if not os.path.exists(fileB):
            print(fileB, "Does not exist")

        if not utilities.file_readable(fileA):
            print(fileA + ": Read permission denied.")
        if not utilities.file_readable(fileB):
            print(fileB + ": Read permission denied.")

        if not utilities.file_writable(fileA):
            print(fileA + ": Write permission denied.")
        if not utilities.file_writable(fileB):
            print(fileB + ": Write permission denied.")

        # prompt = QMessageBox.about(self, "Error", "Error Message")
        fileA = fileOpener.fileAName
        fileB = fileOpener.fileBName

        result = self.fIO.diffFiles(fileA, fileB)

        if result == pmEnums.RESULT.GOOD:
            result = self.fIO.getChangeSets(self.fIO.changesA, self.fIO.changesB)
        elif result == pmEnums.RESULT.BADFILE:
            QMessageBox.about(self, "Error", "Invalid file type")

        tableObj.load_table_contents(fileA, fileB)

    def menuItems(self, tableObj, butn_widget):
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # MENUBAR
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')

        openFileButton = QAction("Open Files", self)
        openFileButton.setShortcut('Ctrl+o')
        openFileButton.triggered.connect(lambda: self.openFile(tableObj))
        fileMenu.addAction(openFileButton)

        saveFileButton = QAction("Save Files", self)
        saveFileButton.setShortcut('Ctrl+s')
        saveFileButton.triggered.connect(tableObj.write_merged_files)
        fileMenu.addAction(saveFileButton)

        mergeLeftButton = QAction("Merge Left", self)
        mergeLeftButton.setShortcut('Ctrl+l')        
        mergeLeftButton.triggered.connect(tableObj.merge_left)
        editMenu.addAction(mergeLeftButton)

        mergeRightButton = QAction("Merge Right", self)
        mergeRightButton.setShortcut('Ctrl+r')        
        mergeRightButton.triggered.connect(tableObj.merge_right)
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

        HideShowButtons = QAction("Hide/Show Buttons", self)
        #no shortcut
        HideShowButtons.triggered.connect(lambda: self.hideShowButns(butn_widget))
        viewMenu.addAction(HideShowButtons)

    def hideShowButns(self, butn_widget):        
        if butn_widget.isVisible():
            butn_widget.hide()
        else:
            butn_widget.show()

def startMain(fileA=0, fileB=0):
    app = QApplication(sys.argv)
    ex = mainWindow(fileA, fileB)
    sys.exit(app.exec_())

