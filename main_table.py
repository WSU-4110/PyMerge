# PyQt imports
from PyQt5.QtWidgets import (
    QTableView,
    QHeaderView,
    QLineEdit,
    QAbstractItemView,
    QPushButton,
    QMainWindow,
    QApplication,
    QWidget,
    QAction,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QGridLayout,
)
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt

# Standard imports
from copy import deepcopy
import os

# Project imports
import gui_config
import utilities as util
import undo_redo
import pmEnums
import fileIO
from changeSet import ChangeSet
undo_ctrlr = undo_redo.UndoRedo(10)


class Row(QtCore.QObject):
    __slots__ = ["row", "table", "right_text", "left_text", "line_num", "change_state_flags"]

    def __init__(
        self,
        row: int,
        table,
        right_text: str or None,
        left_text: str or None,
        line_num: int,
        change_flags: list,
    ):
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
        self.change_state_flags = deepcopy(change_flags)

        # Set the left side background colors
        if self.change_state_flags[0] == pmEnums.CHANGEDENUM.CHANGED:
            self.table.item(self.row_num, gui_config.LEFT_TXT_COL_IDX).setBackground(
                gui_config.COLORS["LINE_DIFF"]
            )
            self.add_row_merge_buttons()

        elif self.change_state_flags[0] == pmEnums.CHANGEDENUM.ADDED:
            self.table.item(self.row_num, gui_config.LEFT_TXT_COL_IDX).setBackground(
                gui_config.COLORS["PAD_SPACE"]
            )
            self.add_row_merge_buttons()

        elif self.change_state_flags[0] == pmEnums.CHANGEDENUM.SAME:
            self.table.item(self.row_num, gui_config.LEFT_TXT_COL_IDX).setBackground(
                gui_config.COLORS["DEFAULT"]
            )

        # Set the right side background colors
        if self.change_state_flags[1] == pmEnums.CHANGEDENUM.CHANGED:
            self.table.item(self.row_num, gui_config.RIGHT_TXT_COL_IDX).setBackground(
                gui_config.COLORS["LINE_DIFF"]
            )
            self.add_row_merge_buttons()

        elif self.change_state_flags[1] == pmEnums.CHANGEDENUM.ADDED:
            self.table.item(self.row_num, gui_config.RIGHT_TXT_COL_IDX).setBackground(
                gui_config.COLORS["PAD_SPACE"]
            )
            self.add_row_merge_buttons()

        elif self.change_state_flags[1] == pmEnums.CHANGEDENUM.SAME:
            self.table.item(self.row_num, gui_config.RIGHT_TXT_COL_IDX).setBackground(
                gui_config.COLORS["DEFAULT"]
            )

        self.table.repaint()

    def add_row_merge_buttons(self):
        right_button = QPushButton(self.table)
        right_icon = QIcon(gui_config.ICONS["MERGE_RIGHT"])
        right_button.setIcon(right_icon)
        right_button.clicked.connect(self.merge_right)
        self.table.setCellWidget(self.line_num, 2, right_button)

        left_button = QPushButton(self.table)
        left_icon = QIcon(gui_config.ICONS["MERGE_LEFT"])
        left_button.setIcon(left_icon)
        left_button.clicked.connect(self.merge_left)
        self.table.setCellWidget(self.line_num, 3, left_button)

    @pyqtSlot()
    def merge_right(self):
        """
        Merge lines from the right to the left
        :return: No return value
        """
        # Copy the left text to the right side
        self.table.setItem(self.row_num, gui_config.LEFT_TXT_COL_IDX, QTableWidgetItem(self.left_text))
        self.table.item(self.row_num,gui_config.LEFT_TXT_COL_IDX).setText(self.left_text)
        self.right_text = self.left_text

        # Set the background colors accordingly. We need a change flag to determine the color to use
        self.table.item(self.row_num, gui_config.LEFT_TXT_COL_IDX).setBackground(gui_config.COLORS["LINE_MERGE"])
        self.table.item(self.row_num, gui_config.RIGHT_TXT_COL_IDX).setBackground(gui_config.COLORS["LINE_MERGE"])

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
        self.table.setItem(self.row_num, gui_config.RIGHT_TXT_COL_IDX, QTableWidgetItem(self.right_text))
        self.table.item(self.row_num, gui_config.RIGHT_TXT_COL_IDX).setText(self.right_text)
        self.left_text = self.right_text

        # Set the background colors accordingly. We need a change flag to determine the color to use
        self.table.item(self.row_num, gui_config.LEFT_TXT_COL_IDX).setBackground(gui_config.COLORS["LINE_MERGE"])
        self.table.item(self.row_num, gui_config.RIGHT_TXT_COL_IDX).setBackground(gui_config.COLORS["LINE_MERGE"])

        # This is a significant user action so we need to record the change in the undo stack
        undo_ctrlr.record_action(self)

        # Table isn't gonna repaint itself. Gotta show users the changes we just made.
        self.table.repaint()


class MainTable(QWidget):
    def __init__(self, change_set_a, change_set_b):
        """
        Initialize the MainTable class
        """        
        super().__init__()
                
        self.rows: list = []
        grid = QGridLayout()
        self.setLayout(grid)
        self.table = QTableWidget()
        self.table.setRowCount(0)  # Set the initial row count to 0
        self.table.setColumnCount(5)  # Set the column count to 5
        self.setAcceptDrops(True)

        # List containing indices of all diff rows. This is used for jump to diff functions
        self.diff_indices: list = []
        self.change_set_a = change_set_a
        self.change_set_b = change_set_b

        # Contains the index of the current diff that has been jumped to
        self.curr_diff_idx: int = 0

        # Set the head text
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Line"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem(""))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Merge\nRight"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Merge\nLeft "))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem(""))

        # Set the header font
        self.table.horizontalHeader().setFont(gui_config.FONTS["TBL_HEADER_DEFAULT"])

        # Set the header text alignment
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)
        self.table.horizontalHeaderItem(3).setTextAlignment(Qt.AlignCenter)
        self.table.horizontalHeaderItem(4).setTextAlignment(Qt.AlignCenter)

        # Set the header background colors
        self.table.horizontalHeaderItem(0).setBackground(
            gui_config.COLORS["TBL_HEADER_DEFAULT_BACKGROUND"]
        )
        self.table.horizontalHeaderItem(1).setBackground(
            gui_config.COLORS["TBL_HEADER_DEFAULT_BACKGROUND"]
        )
        self.table.horizontalHeaderItem(2).setBackground(
            gui_config.COLORS["TBL_HEADER_DEFAULT_BACKGROUND"]
        )
        self.table.horizontalHeaderItem(3).setBackground(
            gui_config.COLORS["TBL_HEADER_DEFAULT_BACKGROUND"]
        )
        self.table.horizontalHeaderItem(4).setBackground(
            gui_config.COLORS["TBL_HEADER_DEFAULT_BACKGROUND"]
        )
        self.table.setGridStyle(Qt.PenStyle(Qt.DotLine))
        self.table.verticalHeader().setVisible(False)

        # Set column resize modes
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

        # Make the table read only for the user
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        grid.addWidget(self.table)

    def dragEnterEvent(self, event):
        """
        Override the dragEnterEvent method from PyQt
        :param event:
        :return:
        """
        event.accept() if event.mimeData().hasUrls else event.ignore()

    def dragMoveEvent(self, event):
        """
        Override the dragMoveEvent method from PyQt
        :param event:
        :return:
        """
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Override the dropEvent method
        :param event:
        :return:
        """
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = event.mimeData().urls()[0]
            print(links)
        else:
            event.ignore()

    @pyqtSlot()
    def goto_next_diff(self):
        """
        Scrolls the table window to the next difference incrementally (starts at the first diff)
        :return: No return value
        """
        
        print("next diffe slot")
        # TODO: Implement goto_next_diff function
        return

    
    @pyqtSlot()
    def goto_prev_diff(self):
        """
        Scrolls the table window to the previous difference incrementally
        :return: No return value
        """
        # TODO: Implement goto_prev_diff function
        print("goto_prev_diff in main_table.py")
    
    @pyqtSlot()
    def undo_last_change(self):
        """
        undoes last change or group of changes
        :return: No return value
        """
        # TODO: Implement 
        print("undo last")

    @pyqtSlot()
    def redo_last_undo(self):
        """
        redo last undo performed
        :return: No return value
        """
        # TODO: Implement 
        print("redo last")
    
    
    def jump_to_line(self, line_num, col=0):
        self.table.scrollToItem(
            self.table.item(line_num, col), QtWidgets.QAbstractItemView.PositionAtTop
        )
        self.table.scrollToItem(
            self.table.selectRow(line_num), QtWidgets.QAbstractItemView.PositionAtTop
        )

    def add_line(self, right_text: str, left_text: str, line_num: int or str, change_flags, left_line_num=0, right_line_num=0):
        """
        Add a row into the table using the right and left text provided as parameters.
        :param right_text: Right text to display
        :param left_text: Left text to display
        :param line_num: Line number to display. This isn't exactly where it's inserted, just a display value
        :param change_flags:
        :return: No return value

        """
        self.table.insertRow(line_num)
        #self.table.setItem(line_num, 0, QTableWidgetItem(str(line_num + 1)))
        self.table.setItem(line_num, 0, QTableWidgetItem(str(line_num + 1)))
        self.table.setItem(line_num, 1, QTableWidgetItem(str(right_text)))
        self.table.setItem(line_num, 2, QTableWidgetItem(""))
        self.table.setItem(line_num, 3, QTableWidgetItem(""))
        self.table.setItem(line_num, 4, QTableWidgetItem(str(left_text)))

        self.table.item(line_num, 0).setTextAlignment(Qt.AlignCenter)
        self.table.item(line_num, 2).setTextAlignment(Qt.AlignCenter)
        self.table.item(line_num, 3).setTextAlignment(Qt.AlignCenter)

        self.table.item(line_num, 0).setBackground(
            gui_config.COLORS["TBL_LINE_COL_DEFAULT_BACKGROUND"]
        )
        self.table.item(line_num, 2).setBackground(
            gui_config.COLORS["TBL_LINE_COL_DEFAULT_BACKGROUND"]
        )
        self.table.item(line_num, 3).setBackground(
            gui_config.COLORS["TBL_LINE_COL_DEFAULT_BACKGROUND"]
        )
        self.table.item(line_num, 4).setBackground(
            gui_config.COLORS["TBL_LINE_COL_DEFAULT_BACKGROUND"]
        )

        row_instance = Row(line_num, self.table, right_text, left_text, line_num, change_flags)
        self.rows.append(row_instance)

    def get_lines_from_tbl(self) -> list:
        """
        Gets the data from the table and returns it as a 2D list.
        :return: list containing right and left hand file data
        """
        return [[row.right_text, row.left_text] for row in self.rows]

    def load_table_contents(self, left_lines: list or dict, right_lines: list or dict, file1, file2):
        # TODO: Add type hints
        """
        Load the contents of two data structures containing the lines to be displayed, into the tables
        :param left_lines: left hand data to show
        :param right_lines: right hand data to show
        :return: No return value
        """

        self.table.horizontalHeaderItem(1).setText(os.path.abspath(file1))
        self.table.horizontalHeaderItem(4).setText(os.path.abspath(file2))

        # Get the change information for each line. Skip the last line, as that is the
        # match token that has been appened on by diff_set in order to capture entire file
        # contents.
        for n in range(len(self.change_set_a.changeList) - 1):
            data_a = [""]
            data_b = [""]
            change_type_a = [pmEnums.CHANGEDENUM.SAME]
            change_type_b = [pmEnums.CHANGEDENUM.SAME]
            self.change_set_a.getChange(n, change_type_a, data_a)
            self.change_set_b.getChange(n, change_type_b, data_b)

            self.add_line(data_a[0], data_b[0], n, [change_type_a[0], change_type_b[0]])

    def load_test_files(self, file1: str, file2: str):
        """
        Load two arbitrary files as as test
        :param file1: right hand file to load
        :param file2: left hand file to load
        :return: No return value
        """
        self.table.horizontalHeaderItem(1).setText(os.path.abspath(file1))
        self.table.horizontalHeaderItem(4).setText(os.path.abspath(file2))

        with open(file1, "r") as file:
            file1_contents = file.read().splitlines()

        with open(file2, "r") as file:
            file2_contents = file.read().splitlines()

        self.load_table_contents(file1_contents, file2_contents)
        self.jump_to_line(77)
