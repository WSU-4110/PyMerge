#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Initial Window
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
import ntpath

# from mainWindow import mainWindow
import mainWindow

from PyQt5 import QtGui
import controlButtons
import main_table
import fileIO
import pmEnums
import diff_resolution
import fileOpenDialog
import os.path
import utilities
from PyQt5 import QtCore


class initialWindow(QMainWindow, QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyMerge-init")
        self.setGeometry(500, 250, 500, 250)
        # self.setGeometry(1000, 1000, 2000, 1000)
        self.fileA = ""
        self.fileB = ""
        layout = QGridLayout()

        self.file_label1 = QLabel(self)
        self.file_label2 = QLabel(self)

        importFile1Button = QPushButton('import file', self)
        importFile1Button.resize(100,50)
        importFile1Button.move(50, 75)
        importFile1Button.clicked.connect(self.import_file1_on_click)

        importFile2Button = QPushButton('import file', self)
        importFile2Button.resize(100, 50)
        importFile2Button.move(350, 75)
        importFile2Button.clicked.connect(self.import_file2_on_click)

        compare = QPushButton('compare', self)
        compare.resize(100, 30)
        compare.move(200, 85)
        compare.setStyleSheet("background-color: #5B6FFF")
        compare.clicked.connect(self.switch_to_main_window)

        self.show()

    @pyqtSlot()
    def import_file1_on_click(self):
        print('Importing file 1')
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.fileA = filename

        self.file_label1.setText(ntpath.basename(self.fileA))
        self.file_label1.move(60, 150)
        self.file_label1.show()

    @pyqtSlot()
    def import_file2_on_click(self):
        print('Importing file 2')
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.fileB = filename

        self.file_label2.setText(ntpath.basename(self.fileB))
        self.file_label2.move(360, 150)
        self.file_label2.show()

    @pyqtSlot()
    def switch_to_main_window(self):
        print("switching to main window")
        print(self.fileA)
        print(self.fileB)

        # self.window = QtWidgets.QMainWindow
        # self.ui = mainWindow(self.fileA, self.fileB)
        # self.window.show()

        self.hide()
        # self.window = QtWidgets.QMainWindow
        # QtGui.QDialog.closeEvent(self, event)
        mainWindow.startMain(self.fileA, self.fileB)

def startMain():
    app = QApplication(sys.argv)
    ex = initialWindow()
    sys.exit(app.exec_())

