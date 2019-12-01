#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import ControlButtons
import main_table
import FileIO
import pmEnums
import diff_resolution
import FileOpenDialog
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


