import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QTableView,
    QHeaderView,
    QLineEdit,
    QAbstractItemView
)

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import gui_config

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


class MainTable(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        self.setLayout(grid)
        self.table = QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(5)

        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 300)

        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Line"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem(""))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Merge Right"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Merge Left"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem(""))
        self.table.verticalHeader().setVisible(False)

        # Set column resize modes
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        grid.addWidget(self.table)

    def add_line(self, right_text, left_text, line_num):
        self.table.insertRow(line_num)
        self.table.setItem(line_num, 0, QTableWidgetItem(str(right_text)))
        self.table.setItem(line_num, 1, QTableWidgetItem(""))
        self.table.setItem(line_num, 2, QTableWidgetItem(""))
        self.table.setItem(line_num, 3, QTableWidgetItem(str(left_text)))

        row_instance = Row(line_num, self.table, right_text, left_text)

        right_button = QtWidgets.QPushButton(self.table)
        right_icon = QtGui.QIcon(gui_config.ICONS["MERGE_RIGHT"])
        right_button.setIcon(right_icon)
        right_button.clicked.connect(row_instance.merge_right)
        self.table.setCellWidget(line_num, 1, right_button)
        self.rows.append(row_instance)

        left_button = QtWidgets.QPushButton(self.table)
        left_icon = QtGui.QIcon(gui_config.ICONS["MERGE_RIGHT"])
        left_button.setIcon(left_icon)
        left_button.clicked.connect(row_instance.merge_left)
        self.table.setCellWidget(line_num, 2, left_button)
        self.rows.append(row_instance)