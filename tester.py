from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QGridLayout, QGroupBox

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, databaseFilePath, userFilePath):
        super(MainWindow,self).__init__()
        self.databaseFilePath = databaseFilePath
        self.userFilePath = userFilePath
        self.createUI()
        self.createBut()

    def createBut(self):
        grid = QGridLayout()        
        grid.setColumnStretch(1, 3)
        self.setLayout()
        
        pyBut1 = QPushButton('Merge Left', self)
        grid.addWidget(pyBut1, 0, 0) 
        pyBut2 = QPushButton('Next Change', self)
        grid.addWidget(pyBut2, 1, 0)
        pyBut3 = QPushButton('Merge Right', self)
        grid.addWidget(pyBut3, 2, 0)

    def changeFilePath(self):
        print('changeFilePath')
        # self.userFilePath = functions_classes.changeFilePath()
        # functions_classes.storeFilePath(self.userFilePath, 1)

    def createUI(self):
        self.setWindowTitle('Equipment Manager 0.3')
        menu = self.menuBar().addMenu('File')
        action = menu.addAction('Change File Path')
        action.triggered.connect(self.changeFilePath)   

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow('some/path', 'some/other/path')
    window.show()
    window.setGeometry(500, 300, 300, 300)
    sys.exit(app.exec_())
