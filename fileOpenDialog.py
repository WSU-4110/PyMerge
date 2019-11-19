import sys

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog


class fileOpenDialog(QWidget):    
    def __init__(self):
        super().__init__()
        self.fileAName = ""
        self.fileBName = ""
        self.title = 'Open FileA'
        if( self.fileAName != "" ):
            self.title = 'Open FileB'
        self.setGeometry(100, 100, 400, 500)
        
        
        


      
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
