#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Initial Window
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtGui
import controlButtons
import main_table
import fileIO
import pmEnums
import diff_resolution
import fileOpenDialog
import os.path
import utilities


class initialWindow(QMainWindow, QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyMerge-init")
        self.setGeometry(500, 250, 500, 250)
        layout = QGridLayout()

        # widget = QWidget()
        # widget.setLayout(layout)
        # self.setCentralWidget(widget)

        importFile1Button = QPushButton('import file', self)
        importFile1Button.resize(100,50)
        importFile1Button.move(83, 75)
        importFile1Button.clicked.connect(self.import_file1_on_click)

        importFile2Button = QPushButton('import file', self)
        importFile2Button.resize(100, 50)
        importFile2Button.move(300, 75)
        importFile2Button.clicked.connect(self.import_file2_on_click)

        self.show()

    @pyqtSlot()
    def import_file1_on_click(self):
        print('Importing file 1')

    @pyqtSlot()
    def import_file2_on_click(self):
        print('Importing file 2')

def startMain():
    app = QApplication(sys.argv)
    ex = initialWindow()
    sys.exit(app.exec_())

