
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

    def __init__(self, row: int, table, right_text: str or None, left_text: str or None, line_num: int):
        """
        Initialize the Row class instance
        :param row: row number
        :param table: table widget instance
        :param right_text: string containing the right side text
        :param left_text: string containg the left side text
        :param line_num:
        """
        super().__init__()
        self.row_num: int = row
        self.table = table
        self.right_text: str = right_text
        self.left_text: str = left_text
        self.line_num: int = line_num
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
        """
        Merge lines from the right to the left
        :return: No return value
        """
        # Copy the left text to the right side
        self.table.setItem(self.row_num, 1, QTableWidgetItem(self.left_text))
        self.table.item(self.row_num, 1).setText(self.left_text)
        self.right_text = self.left_text

        # Set the background colors accordingly. We need a change flag to determine the color to use
        self.table.item(self.row_num, 1).setBackground(gui_config.COLORS["LINE_MERGE"])

        # This is a significant user action so we need to record the change in the undo stack
        undo_ctrlr.record_action(self)

        # Table isn't gonna repaint itself. Gotta show users the changes we just made.
        self.table.repaint()

    @pyqtSlot()
    def merge_left(self):
        """
        Merge lines from the left to the right
        :return: No return value
        """
        # Copy the right text to the right side
        self.table.setItem(self.row_num, 4, QTableWidgetItem(self.right_text))
        self.table.item(self.row_num, 4).setText(self.right_text)
        self.left_text = self.right_text

        # Set the background colors accordingly. We need a change flag to determine the color to use
        self.table.item(self.row_num, 4).setBackground(gui_config.COLORS["LINE_MERGE"])

        # This is a significant user action so we need to record the change in the undo stack
        undo_ctrlr.record_action(self)

        # Table isn't gonna repaint itself. Gotta show users the changes we just made.
        self.table.repaint()


class MainTable(QWidget):
    def __init__(self):
        """
        Initialize the MainTable class
        """
        super().__init__()
        self.rows: list = []
        grid = QGridLayout()
        self.setLayout(grid)
        self.table = QTableWidget()
        self.table.setRowCount(0)   # Set the initial row count to 0
        self.table.setColumnCount(5)    # Set the column count to 5

        # Set the head text
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Line"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem(""))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Merge Right"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Merge Left"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem(""))

        # Set the header font
        self.table.horizontalHeader().setFont(gui_config.FONTS["TBL_HEADER_DEFAULT"])

        # Set the header text alignment
        self.table.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.horizontalHeaderItem(3).setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.horizontalHeaderItem(4).setTextAlignment(QtCore.Qt.AlignCenter)

        # Set the header background colors
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

        # Make the table read only for the user
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        grid.addWidget(self.table)

    def add_line(self, right_text: str, left_text: str, line_num: int or str):
        """
        Add a row into the table using the right and left text provided as parameters.
        :param right_text: Right text to display
        :param left_text: Left text to display
        :param line_num: Line mumber to display. This isn't exactly where it's inserted, just a display value
        :return: No return value
        """
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
        # TODO: Add type hints
        """
        Load the contents of two data structures containing the lines to be displayed, into the tables
        :param left_lines: left hand data to show
        :param right_lines: right hand data to show
        :return: No return value
        """
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

    def load_test_files(self, file1: str, file2: str):
        """
        Load two arbitrary files as as test
        :param file1: right hand file to load
        :param file2: left hand file to load
        :return: No return value
        """
        self.table.horizontalHeaderItem(1).setText(os.path.abspath(file1))
        self.table.horizontalHeaderItem(4).setText(os.path.abspath(file2))

        with open(file1, 'r') as file:
            file1_contents = file.read().splitlines()

        with open(file2, 'r') as file:
            file2_contents = file.read().splitlines()

        self.load_table_contents(file1_contents, file2_contents)