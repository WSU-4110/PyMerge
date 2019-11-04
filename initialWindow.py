#!/usr/bin/python3

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

class initialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Initial Window")
        self.setGeometry(1000, 1000, 2000, 1000)

def startWindow():
    app = QApplication(sys.argv)
    ex = initialWindow()
    # sys.exit(app.exec_())


