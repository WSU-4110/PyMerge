#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Initial Window
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
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
    def __init__(self, fileA=0, fileB=0):
        super().__init__()
        self.setWindowTitle("PyMerge-init")
        self.setGeometry(500, 250, 500, 250)
        layout = QGridLayout()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(500, 70)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

def startMain(fileA=0, fileB=0):
    app = QApplication(sys.argv)
    ex = initialWindow(fileA, fileB)
    sys.exit(app.exec_())

