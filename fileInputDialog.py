# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TextBoxDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FileInputDialog(object):
    def setupUi(self, FileInputDialog):
        FileInputDialog.setObjectName("FileInputDialog")
        FileInputDialog.resize(379, 146)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FileInputDialog.sizePolicy().hasHeightForWidth())
        FileInputDialog.setSizePolicy(sizePolicy)
        FileInputDialog.setWindowTitle("Open Files")
        self.buttonBox = QtWidgets.QDialogButtonBox(FileInputDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 100, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.FileA = QtWidgets.QLineEdit(FileInputDialog)
        self.FileA.setGeometry(QtCore.QRect(30, 20, 331, 21))
        self.FileA.setText("")
        self.FileA.setObjectName("FileA")
        self.FileB = QtWidgets.QLineEdit(FileInputDialog)
        self.FileB.setGeometry(QtCore.QRect(30, 60, 331, 21))
        self.FileB.setText("")
        self.FileB.setObjectName("FileB")

        self.retranslateUi(FileInputDialog)
        self.buttonBox.accepted.connect(FileInputDialog.accept)
        self.buttonBox.rejected.connect(FileInputDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FileInputDialog)

    def retranslateUi(self, FileInputDialog):
        _translate = QtCore.QCoreApplication.translate
        self.FileA.setPlaceholderText(_translate("FileInputDialog", "File A"))
        self.FileB.setPlaceholderText(_translate("FileInputDialog", "File B"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FileInputDialog = QtWidgets.QDialog()
    ui = Ui_FileInputDialog()
    ui.setupUi(FileInputDialog)
    FileInputDialog.show()
    sys.exit(app.exec_())

