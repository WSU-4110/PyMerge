import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
import pmEnums, fileIO

class fileOpenDialog(QWidget):    
    def __init__(self):
        super().__init__()
        print("wtf")
        self.fileAName = ""
        self.fileBName = ""
        self.title = 'Open FileA'
        if( self.fileAName != "" ):
            self.title = 'Open FileB'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.openFileNameDialog()
        self.openFileNameDialog()
      
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        if( self.fileAName == "" ):
            self.fileAName, _ = QFileDialog.getOpenFileName(self,"Open File A", "","", options=options)
        else:
            self.fileBName, _ = QFileDialog.getOpenFileName(self,"Open File B", "","", options=options)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = fileOpenDialog()
    sys.exit(app.exec_())