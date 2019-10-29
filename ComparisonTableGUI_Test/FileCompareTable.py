import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout


class Row(QtCore.QObject):
    def __init__(self, row, table, right_text, left_text):
        super().__init__()
        self.row_num = row
        self.table = table
        self.right_text = right_text
        self.left_text = left_text

    @pyqtSlot()
    def merge_right(self):
        self.table.setItem(self.row_num, 0, QTableWidgetItem(self.left_text))
        self.table.item(self.row_num, 0).setText(self.left_text)
        self.table.repaint()
        self.right_text = self.left_text

    @pyqtSlot()
    def merge_left(self):
        self.table.setItem(self.row_num, 3, QTableWidgetItem(self.right_text))
        self.table.item(self.row_num, 0).setText(self.right_text)
        self.table.repaint()
        self.left_text = self.right_text


class App(QWidget):
    def __init__(self, file1, file2):
        super().__init__()
        self.file1 = file1
        self.file2 = file2
        self.title = 'PyMerge'
        self.left = 0
        self.top = 0
        self.width = 1700
        self.height = 800
        self.rows = []

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_table()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)



        self.setLayout(self.layout)
        self.show()

    def add_line(self, right_text, left_text, line_num):
        self.table.insertRow(line_num)
        self.table.setItem(line_num, 0, QTableWidgetItem(str(right_text)))
        self.table.setItem(line_num, 1, QTableWidgetItem(""))
        self.table.setItem(line_num, 2, QTableWidgetItem(""))
        self.table.setItem(line_num, 3, QTableWidgetItem(str(left_text)))

        row_instance = Row(line_num, self.table, right_text, left_text)

        right_button = QtWidgets.QPushButton(self.table)
        right_icon = QtGui.QIcon('left-arrow.png')
        right_button.setIcon(right_icon)
        right_button.clicked.connect(row_instance.merge_right)
        self.table.setCellWidget(line_num, 1, right_button)
        self.rows.append(row_instance)

        left_button = QtWidgets.QPushButton(self.table)
        left_icon = QtGui.QIcon('right-arrow.png')
        left_button.setIcon(left_icon)
        left_button.clicked.connect(row_instance.merge_left)
        self.table.setCellWidget(line_num, 2, left_button)
        self.rows.append(row_instance)

    def create_table(self):
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(4)

        self.table.setColumnWidth(0, 700)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 700)

        self.table.setHorizontalHeaderItem(0, QTableWidgetItem(""))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Merge Right"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Merge Left"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem(""))

        if self.file1 == "" and self.file2 == "":
            file1_contents = []
            file2_contents = []
        else:
            with open(self.file1, 'r') as file:
                file1_contents = file.read().splitlines()
            with open(self.file2, 'r') as file:
                file2_contents = file.read().splitlines()

        # Make lists equal length (needs different implementation obviously)
        if len(file1_contents) > len(file2_contents):
            for n in range(len(file1_contents) - len(file2_contents)):
                file2_contents.append("")
        elif len(file2_contents) > len(file1_contents):
            for n in range(len(file2_contents) - len(file1_contents)):
                file1_contents.append("")

        for n in range(len(file1_contents)):
            self.add_line(file1_contents[n], file2_contents[n],  n)

        self.table.move(0, 0)


def run_app(file1, file2):
    app = QApplication(sys.argv)
    ex = App(file1, file2)
    sys.exit(app.exec_())

run_app("file1.c", "file2.c")
