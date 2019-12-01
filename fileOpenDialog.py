import sys

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog


class fileOpenDialog(QWidget):    
    def __init__(self):
        super().__init__()
        self.fileName = ""
        self.title = 'Open File'
        self.setGeometry(100, 100, 400, 500)
              
    def openFileNameDialog(self):        
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self,"Open File A", "","", options=options)    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = fileOpenDialog()
    sys.exit(app.exec_())
