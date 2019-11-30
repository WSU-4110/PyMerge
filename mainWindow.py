#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main Window
"""

import os.path
import subprocess
import sys

from PyQt5.QtWidgets import *

import controlButtons
import fileIO
import fileOpenDialog
import main_table
import pmEnums
import utilities


class mainWindow(QMainWindow, QMessageBox):
    def __init__(self, fileA=0, fileB=0):
        super().__init__()
        self.setWindowTitle("PyMerge")
        self.setGeometry(10, 50, 1750, 900)
        self.table_widget = 0
        self.control_buttons_widget = 0
        layout = QGridLayout()

        # load files and generate changesets
        result = pmEnums.RESULT.ERROR
        self.fIO = fileIO.fileIO()
        if fileA != 0 and fileB != 0:
            result = self.fIO.diffFiles(fileA, fileB)
            if result == pmEnums.RESULT.GOOD:
                result = self.fIO.getChangeSets(self.fIO.changesA, self.fIO.changesB)

        self.table_widget = 0   
        #load table
        self.table_widget = main_table.MainTable(self.fIO.changesA, self.fIO.changesB)            
        #add table

        layout.addWidget(self.table_widget, 1, 0)

        #load table with fileA and B if present from command line
        if fileA != 0 and fileB != 0:
            self.table_widget.load_table_contents(fileA, fileB)  # Left list arguments for now
        self.table_widget.load_table_contents()  # Left list arguments for now
        
        self.control_buttons_widget = controlButtons.controlButtons(self.table_widget)
        layout.addWidget(self.control_buttons_widget, 0, 0)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.initUI()

    def initUI(self):
        # start GUI

        self.menuItems()
        self.show()

    def openFile(self):

        self.table_widget.clear_table()
        
        fileOpenerA = fileOpenDialog.fileOpenDialog()
        fileOpenerB = fileOpenDialog.fileOpenDialog()
        
        fileOpenerA.openFileNameDialog()
        fileA = fileOpenerA.fileName
        
        if fileA != "":
            fileOpenerB.openFileNameDialog()        
        fileB = fileOpenerB.fileName
        
        result = self.fIO.diffFiles(fileA, fileB)

        if result == pmEnums.RESULT.GOOD:
            result = self.fIO.getChangeSets(self.fIO.changesA, self.fIO.changesB)

        elif result == pmEnums.RESULT.BADFILE:
            QMessageBox.about(self, "Error", "Invalid file type")

            
        self.table_widget.load_table_contents(fileA, fileB)
        return result

    def menuItems(self):
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # MENUBAR
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        helpMenu = mainMenu.addMenu('Help')
        
        openFileButton = QAction("Open Files", self)
        openFileButton.setShortcut('Ctrl+o')
        openFileButton.triggered.connect(lambda: self.openFile())
        fileMenu.addAction(openFileButton)

        saveFileButton = QAction("Save Files", self)
        saveFileButton.setShortcut('Ctrl+s')
        saveFileButton.triggered.connect(self.table_widget.write_merged_files)
        fileMenu.addAction(saveFileButton)

        mergeLeftButton = QAction("Merge Left", self)
        mergeLeftButton.setShortcut('Ctrl+l')        
        mergeLeftButton.triggered.connect(self.table_widget.merge_left)
        editMenu.addAction(mergeLeftButton)

        mergeRightButton = QAction("Merge Right", self)
        mergeRightButton.setShortcut('Ctrl+r')        
        mergeRightButton.triggered.connect(self.table_widget.merge_right)
        editMenu.addAction(mergeRightButton)

        previousDiffButn = QAction("Previous Difference", self)
        previousDiffButn.setShortcut('Ctrl+p')
        previousDiffButn.triggered.connect(self.table_widget.goto_prev_diff)
        editMenu.addAction(previousDiffButn)

        nextDiffButn = QAction("Next Difference", self)
        nextDiffButn.setShortcut('Ctrl+n')
        nextDiffButn.triggered.connect(self.table_widget.goto_next_diff)
        editMenu.addAction(nextDiffButn)

        undoChangeButn = QAction("Undo", self)
        undoChangeButn.setShortcut('Ctrl+z')
        undoChangeButn.triggered.connect(self.table_widget.undo_last_change)
        editMenu.addAction(undoChangeButn)

        redoChangeButn = QAction("Redo", self)
        redoChangeButn.setShortcut('Ctrl+y')
        redoChangeButn.triggered.connect(self.table_widget.redo_last_undo)
        editMenu.addAction(redoChangeButn)

        HideShowButtons = QAction("Hide/Show Buttons", self)
        #no shortcut
        HideShowButtons.triggered.connect(lambda: self.hideShowButns())
        viewMenu.addAction(HideShowButtons)

        HelpButton = QAction("Manual", self)
        #no shortcut
        HelpButton.triggered.connect(lambda: self.openHelp())
        helpMenu.addAction(HelpButton)
        

    def hideShowButns(self):        
        if self.control_buttons_widget.isVisible():
            self.control_buttons_widget.hide()
        else:
            self.control_buttons_widget.show()

    def openHelp(self):
        subprocess.Popen("PyMerge_Manual.pdf",shell=True)

def startMain(fileA=0, fileB=0):
    app = QApplication(sys.argv)
    ex = mainWindow(fileA, fileB)
    sys.exit(app.exec_())

