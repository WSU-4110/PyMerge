#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main Window
"""

import os.path
import subprocess
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui
import controlButtons
import fileIO
import fileOpenDialog
import main_table
import pmEnums
import utilities
import ntpath
import os


class mainWindow(QMainWindow, QMessageBox):
    def __init__(self, fileA=0, fileB=0):
        super().__init__()
        self.setWindowTitle("PyMerge")
        self.setGeometry(100, 100, 1000, 800)
        self.table_widget = 0
        self.control_buttons_widget = 0
        layout = QGridLayout()

        self.file1 = ""
        self.file2 = ""

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

        self.control_buttons_widget = controlButtons.controlButtons(self.table_widget, self)
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

        # self.statusBar().showMessage('Opening file...')

        # self.table_widget.clear_table()

        print("\n\n" +  str(type(self)) + "\n\n")

        fileOpener = fileOpenDialog.fileOpenDialog()
        fileOpener.openFileNameDialog()

        if fileOpener.fileAName != "":
            fileOpener.openFileNameDialog()

        fileA = fileOpener.fileAName
        fileB = fileOpener.fileBName

        self.openFileHelper(fileA, fileB)

        # self.statusBar().clearMessage()

    def openFileHelper(self, fileA, fileB):

        if utilities.file_writable(fileA):
            QMessageBox.about(self, "Error", os.path.basename(fileA) + " is not writable")
            return
        if utilities.file_writable(fileB):
            QMessageBox.about(self, "Error", os.path.basename(fileB) + " is not writable")
            return

        result = self.fIO.diffFiles(fileA, fileB)

        if result == pmEnums.RESULT.GOOD:
            result = self.fIO.getChangeSets(self.fIO.changesA, self.fIO.changesB)

        elif result == pmEnums.RESULT.BADFILE:
            QMessageBox.about(self, "Error", "Invalid file type")

            
        self.table_widget.load_table_contents(fileA, fileB)
        return result

    @pyqtSlot()
    def statusBar(self):
        print("Connect this to methods in main_table.py")

    # def menuItems(self, tableObj):

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

        row = QAction("current row", self)

        HelpButton = QAction("Manual", self)
        #no shortcut
        HelpButton.triggered.connect(lambda: self.openHelp())
        helpMenu.addAction(HelpButton)
        

    def hideShowButns(self):
        if self.control_buttons_widget.isVisible():
            self.control_buttons_widget.hide()
        else:
            self.control_buttons_widget.show()

    @pyqtSlot()
    def import_file1(self):
        print("Importing file 1")
        options = QFileDialog.Options()
        self.file1, _ = QFileDialog.getOpenFileName(self, "Open File A", "","", options=options)

    @pyqtSlot()
    def import_file2(self):
        print("Importing file 2")
        options = QFileDialog.Options()
        self.file2, _ = QFileDialog.getOpenFileName(self, "Open File B", "", "", options=options)

    @pyqtSlot()
    def merge_files(self):
        print("Merging " + ntpath.basename(self.file1) + " and " + ntpath.basename(self.file2))
        self.openFileHelper(self.file1, self.file2)

    def openHelp(self):
        subprocess.Popen("file1.c",shell=True)

def startMain(fileA=0, fileB=0):
    app = QApplication(sys.argv)
    ex = mainWindow(fileA, fileB)
    sys.exit(app.exec_())