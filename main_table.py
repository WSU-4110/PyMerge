# PyQt imports
# Standard imports
import os

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import (
    QHeaderView,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QGridLayout,
)

# Project imports
import gui_config as gui_cfg
import merge_finalizer
import pmEnums
import table_row
import undo_redo


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
        self.undo_ctrlr: undo_redo.UndoRedo = undo_redo.UndoRedo.get_instance()

        # List containing indices of all diff rows. This is used for jump to diff functions
        self.diff_indices: list = []
        # Contains the index of the current diff that has been jumped to
        self.curr_diff_idx: int = -1

        self.change_set_a = change_set_a
        self.change_set_b = change_set_b

        self.table.verticalHeader().setVisible(
            False
        )  # Disable the automatic line numbers.
        self.table.setVerticalScrollMode(0)

        # Set the head text
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Line"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem(""))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Merge\nRight"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Merge\nLeft "))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem(""))

        # Set the header font
        self.table.horizontalHeader().setFont(gui_cfg.FONTS["TBL_HEADER_DEFAULT"])

        # Set the header text alignment
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignCenter)
        self.table.horizontalHeaderItem(3).setTextAlignment(Qt.AlignCenter)
        self.table.horizontalHeaderItem(4).setTextAlignment(Qt.AlignCenter)

        # Set column resize modes
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

        self.set_tbl_fonts_and_colors()  # Set the color and fonts
        self.table.setGridStyle(Qt.PenStyle(Qt.DotLine))

        # Make the table read only for the user
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Convert icon paths from gui_config.py to QIcon objects
        gui_cfg.convert_icon_dict()
        grid.addWidget(self.table)

    def set_tbl_fonts_and_colors(self):
        """
        Contains all the function calls required to setup the color and text formatting for the table.
        :return:
        """
        # Set the header background colors
        self.table.horizontalHeaderItem(0).setBackground(
            gui_cfg.COLORS["TBL_HDR_DEFAULT_BG"]
        )
        self.table.horizontalHeaderItem(1).setBackground(
            gui_cfg.COLORS["TBL_HDR_DEFAULT_BG"]
        )
        self.table.horizontalHeaderItem(2).setBackground(
            gui_cfg.COLORS["TBL_HDR_DEFAULT_BG"]
        )
        self.table.horizontalHeaderItem(3).setBackground(
            gui_cfg.COLORS["TBL_HDR_DEFAULT_BG"]
        )
        self.table.horizontalHeaderItem(4).setBackground(
            gui_cfg.COLORS["TBL_HDR_DEFAULT_BG"]
        )

        # Setup the text and background colors for active and inactive rows (selections)
        table_palette = QtGui.QPalette(self.table.palette())
        table_palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.HighlightedText,
            QtGui.QBrush(gui_cfg.COLORS["ROW_ACTV_TXT"]),
        )
        table_palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.HighlightedText,
            QtGui.QBrush(gui_cfg.COLORS["ROW_INACTV_TXT"]),
        )
        table_palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Highlight,
            QtGui.QBrush(gui_cfg.COLORS["ROW_ACTV_BG"]),
        )
        table_palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Highlight,
            QtGui.QBrush(gui_cfg.COLORS["ROW_INACTV_BG"]),
        )
        self.table.setPalette(table_palette)

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
        if len(self.diff_indices) == 0:
            return
        if self.curr_diff_idx == len(self.diff_indices) - 1:
            self.curr_diff_idx = 0
            self.jump_to_line(self.diff_indices[self.curr_diff_idx])
        else:
            self.curr_diff_idx += 1
            self.jump_to_line(self.diff_indices[self.curr_diff_idx])
        self.table.repaint()
        return

    @pyqtSlot()
    def goto_prev_diff(self):
        """
        Scrolls the table window to the previous difference incrementally
        :return: No return value
        """
        if len(self.diff_indices) == 0:
            return

        if self.curr_diff_idx == 0 or self.curr_diff_idx == -1:
            self.curr_diff_idx = len(self.diff_indices) - 1
            self.jump_to_line(self.diff_indices[self.curr_diff_idx])
        else:
            self.curr_diff_idx -= 1
            self.jump_to_line(self.diff_indices[self.curr_diff_idx])
        self.table.repaint()
        return

    @pyqtSlot()
    def undo_last_change(self):
        """
        undoes last change or group of changes
        :return: No return value
        """

        # TODO: Implement
        self.undo_ctrlr.undo()
        for row in self.rows:
            row.set_row_state()

    @pyqtSlot()
    def redo_last_undo(self):
        """
        redo last undo performed
        :return: No return value
        """
        self.undo_ctrlr.redo()
        for row in self.rows:
            row.set_row_state()

    @pyqtSlot()
    def merge_left(self):
        """
        merge the whole left selection into the right
        """
        indexesList = self.table.selectedIndexes()
        if len(indexesList) != 0:
            print(indexesList[0].data)
        print("merge left")
        return 0

    @pyqtSlot()
    def merge_right(self):
        """
        merge the whole right selection into the right
        """
        print("merge right")
        return 0

    def jump_to_line(self, line_num, col=0):
        self.table.scrollToItem(
            self.table.item(line_num, col), QtWidgets.QAbstractItemView.PositionAtTop
        )
        self.table.scrollToItem(
            self.table.selectRow(line_num), QtWidgets.QAbstractItemView.PositionAtTop
        )

    def add_line(
        self,
        right_text: str,
        left_text: str,
        line_num: int or str,
        change_flags,
        left_line_num=0,
        right_line_num=0,
    ):
        """
        Add a row into the table using the right and left text provided as parameters.
        :param right_text: Right text to display
        :param left_text: Left text to display
        :param line_num: Line number to display. This isn't exactly where it's inserted, just a display value
        :param change_flags:
        :return: No return value

        """
        self.table.insertRow(line_num)
        self.table.setItem(line_num, 0, QTableWidgetItem(str(line_num + 1)))
        self.table.setItem(line_num, 1, QTableWidgetItem(str(right_text)))
        self.table.setItem(line_num, 2, QTableWidgetItem(""))
        self.table.setItem(line_num, 3, QTableWidgetItem(""))
        self.table.setItem(line_num, 4, QTableWidgetItem(str(left_text)))

        self.table.item(line_num, 0).setTextAlignment(Qt.AlignCenter)
        self.table.item(line_num, 2).setTextAlignment(Qt.AlignCenter)
        self.table.item(line_num, 3).setTextAlignment(Qt.AlignCenter)

        self.table.item(line_num, 0).setBackground(
            gui_cfg.COLORS["TBL_LINE_COL_DEFAULT_BG"]
        )
        self.table.item(line_num, 2).setBackground(
            gui_cfg.COLORS["TBL_LINE_COL_DEFAULT_BG"]
        )
        self.table.item(line_num, 3).setBackground(
            gui_cfg.COLORS["TBL_LINE_COL_DEFAULT_BG"]
        )
        self.table.item(line_num, 4).setBackground(
            gui_cfg.COLORS["TBL_LINE_COL_DEFAULT_BG"]
        )

        row_instance = table_row.Row(
            line_num, self.table, right_text, left_text, line_num, change_flags
        )
        self.rows.append(row_instance)

    def get_lines_from_tbl(self) -> list:
        """
        Gets the data from the table and returns it as a 2D list.
        :return: list containing right and left hand file data
        """
        outp_left: list = []
        outp_right: list = []

        for row in self.rows:
            if row.row_deleted[1]:
                outp_left.append(None)
            else:
                outp_left.append(row.left_text)
            if row.row_deleted[0]:
                outp_right.append(None)
            else:
                outp_right.append(row.right_text)

        return [outp_left, outp_right]

    def clear_table(self) -> bool:
        for row in self.rows:
            try:
                self.table.removeRow(row.row_num)
            except (IndexError, Exception):
                print("Error: could not clear main table.")
                return False
        self.rows.clear()
        self.table.setRowCount(0)
        del self.change_set_a.changeList[:]
        del self.change_set_b.changeList[:]
        return True

    def load_table_contents(self, file1=0, file2=0):
        if file1 == 0 or file2 == 0:
            return
        """
        Load the contents of two data structures containing the lines to be displayed, into the tables
        :param left_lines: left hand data to show
        :param right_lines: right hand data to show
        :return: No return value
        """

        self.table.horizontalHeaderItem(1).setText(os.path.abspath(file1))
        self.table.horizontalHeaderItem(4).setText(os.path.abspath(file2))
        self.left_file = file1
        self.right_file = file2

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

        # generate list of diff lines, to enable prev/next diff jump buttons
        n = 0

        while n < len(self.change_set_a.changeList) - 1:
            data_a = [""]
            change_type_a = [pmEnums.CHANGEDENUM.SAME]
            self.change_set_a.getChange(n, change_type_a, data_a)
            if change_type_a[0] != pmEnums.CHANGEDENUM.SAME:
                self.diff_indices.append(n)
                while change_type_a[0] != pmEnums.CHANGEDENUM.SAME:
                    n += 1
                    self.change_set_a.getChange(n, change_type_a, data_a)
            n += 1

    @pyqtSlot()
    def write_merged_files(self):
        merged_file_contents = self.get_lines_from_tbl()
        merge_writer = merge_finalizer.MergeFinalizer(
            self.left_file, self.right_file, "file_backup"
        )
        merge_writer.finalize_merge(
            merged_file_contents[0][:-1], merged_file_contents[1][:-1]
        )

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