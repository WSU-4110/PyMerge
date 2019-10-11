"""
Buttons pressed will call these functions, 
these functions will make the appropriate function calls.
"""

import pmEnums
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QObject
import fileOpenDialog

class buttonActions:
    
    
    nextDiffSignal = pyqtSignal()
    def __init__(self):
        self.nextDiffSignal.connect(MainTable.goto_next_diff)

    
    def mergeLeft():
        print("mergeL")
        return pmEnums.RESULT.NOTIMPL

    def mergeRight():
        print("mergeR")
        return pmEnums.RESULT.NOTIMPL
    
    def openFile(self):
        fileDialog = fileOpenDialog.fileOpenDialog()
        return pmEnums.RESULT.NOTIMPL
    
    def previousDiff():
        print("prev diff")
        return pmEnums.RESULT.NOTIMPL
    
    def nextDiff(self):
        self.nextDiffSignal.emit()
        print("next diff")
        return pmEnums.RESULT.NOTIMPL

    def undoChange():
        print("undo")
        return pmEnums.RESULT.NOTIMPL

    def redoChange():
        print("redo")
        return pmEnums.RESULT.NOTIMPL
