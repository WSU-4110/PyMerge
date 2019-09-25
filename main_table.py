
# PyQt imports
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableView, QHeaderView, QLineEdit, QAbstractItemView
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# Standard imports
from copy import deepcopy
import os
import sys

# Project imports
import gui_config
import undo_redo

undo_ctrlr = undo_redo.Undo(10)


class Row(QtCore.QObject):
    __slots__ = ["row", "table", "right_text", "left_text", "line_num"]

    def __init__(self, row, table, right_text, left_text, line_num):
        super().__init__()
        self.row_num = row
        self.table = table
        self.right_text = right_text
        self.left_text = left_text
        self.line_num = line_num
        self.right_background_color = None
        self.left_background_color = None

        if right_text is None:
            self.table.item(self.row_num, 1).setBackground(gui_config.COLORS["PAD_SPACE"])
        else:
            self.table.item(self.row_num, 1).setBackground(gui_config.COLORS["DEFAULT"])

        if left_text is None:
            self.table.item(self.row_num, 4).setBackground(gui_config.COLORS["PAD_SPACE"])
        else:
            self.table.item(self.row_num, 4).setBackground(gui_config.COLORS["DEFAULT"])

        right_button = QtWidgets.QPushButton(self.table)
        right_icon = QtGui.QIcon(gui_config.ICONS["MERGE_RIGHT"])
        right_button.setIcon(right_icon)
        right_button.clicked.connect(self.merge_right)
        self.table.setCellWidget(self.line_num, 2, right_button)


        left_button = QtWidgets.QPushButton(self.table)
        left_icon = QtGui.QIcon(gui_config.ICONS["MERGE_LEFT"])
        left_button.setIcon(left_icon)
        left_button.clicked.connect(self.merge_left)
        self.table.setCellWidget(line_num, 3, left_button)

        self.table.repaint()

    @pyqtSlot()
    def merge_right(self):
        self.table.setItem(self.row_num, 1, QTableWidgetItem(self.left_text))
        self.table.item(self.row_num, 1).setText(self.left_text)
        self.right_text = self.left_text
        self.table.item(self.row_num, 1).setBackground(gui_config.COLORS["LINE_MERGE"])
        undo_ctrlr.record_action(self)
        self.table.repaint()

    @pyqtSlot()
    def merge_left(self):
        self.table.setItem(self.row_num, 4, QTableWidgetItem(self.right_text))
        self.table.item(self.row_num, 4).setText(self.right_text)
        self.left_text = self.right_text
        self.table.item(self.row_num, 4).setBackground(gui_config.COLORS["LINE_MERGE"])
        undo_ctrlr.record_action(self)
        self.table.repaint()


class MainTable(QWidget):
    def __init__(self):
        super().__init__()

        grid = QGridLayout()
        self.setLayout(grid)
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.rows = []

        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Line"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem(""))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Merge Right"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Merge Left"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem(""))

        self.table.horizontalHeaderItem(0).setFont(gui_config.FONTS["TBL_HEADER_DEFAULT"])
        self.table.horizontalHeaderItem(1).setFont(gui_config.FONTS["TBL_HEADER_DEFAULT"])
        self.table.horizontalHeaderItem(2).setFont(gui_config.FONTS["TBL_HEADER_DEFAULT"])
        self.table.horizontalHeaderItem(3).setFont(gui_config.FONTS["TBL_HEADER_DEFAULT"])
        self.table.horizontalHeaderItem(4).setFont(gui_config.FONTS["TBL_HEADER_DEFAULT"])

        self.table.horizontalHeaderItem(0).setForeground(gui_config.COLORS["TBL_HEADER_DEFAULT_FOREGROUND"])

        self.table.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.horizontalHeaderItem(3).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.horizontalHeaderItem(4).setTextAlignment(QtCore.Qt.AlignCenter)

        self.table.horizontalHeaderItem(0).setBackground(gui_config.COLORS["TBL_HEADER_DEFAULT_BACKGROUND"])
        self.table.horizontalHeaderItem(1).setBackground(gui_config.COLORS["TBL_HEADER_DEFAULT_BACKGROUND"])
        self.table.horizontalHeaderItem(2).setBackground(gui_config.COLORS["TBL_HEADER_DEFAULT_BACKGROUND"])
        self.table.horizontalHeaderItem(3).setBackground(gui_config.COLORS["TBL_HEADER_DEFAULT_BACKGROUND"])
        self.table.horizontalHeaderItem(4).setBackground(gui_config.COLORS["TBL_HEADER_DEFAULT_BACKGROUND"])
        self.table.verticalHeader().setVisible(False)

        # Set column resize modes
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        grid.addWidget(self.table)

    def add_line(self, right_text, left_text, line_num):
        self.table.insertRow(line_num)
        self.table.setItem(line_num, 0, QTableWidgetItem(str(line_num)))
        self.table.setItem(line_num, 1, QTableWidgetItem(str(right_text)))
        self.table.setItem(line_num, 2, QTableWidgetItem(""))
        self.table.setItem(line_num, 3, QTableWidgetItem(""))
        self.table.setItem(line_num, 4, QTableWidgetItem(str(left_text)))

        self.table.item(line_num, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.item(line_num, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.item(line_num, 3).setTextAlignment(QtCore.Qt.AlignCenter)

        row_instance = Row(line_num, self.table, right_text, left_text, line_num)
        self.rows.append(row_instance)

    def load_table_contents(self, left_lines, right_lines):
        left_text_lines = deepcopy(left_lines)
        right_text_lines = deepcopy(right_lines)

        # Pad arrays. Remove this later
        if len(left_text_lines) > len(right_text_lines):
            for n in range(len(left_text_lines)):
                right_text_lines.append("")
        elif len(right_text_lines) > len(left_text_lines):
            for n in range(len(right_text_lines)):
                left_text_lines.append("")

        for n in range(max(len(left_text_lines), len(right_text_lines))):
            self.add_line(left_text_lines[n], right_text_lines[n], n)

    def load_test_files(self, file1, file2):
        self.table.horizontalHeaderItem(1).setText(os.path.abspath(file1))
        self.table.horizontalHeaderItem(4).setText(os.path.abspath(file2))

        with open(file1, 'r') as file:
            file1_contents = file.read().splitlines()

        with open(file2, 'r') as file:
            file2_contents = file.read().splitlines()

        self.load_table_contents(file1_contents, file2_contents)