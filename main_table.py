"""
###########################################################################
File: main_table.py
Author: Malcolm Hall, John Toniolo, Saular Raffi
Description:


Copyright (C) PyMerge Team 2019

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
###########################################################################
"""

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
    QApplication,
    QPushButton,
    QMessageBox
)

import file_io
# Project imports
import gui_config as gui_cfg
import merge_finalizer
import pymerge_enums
import table_row
import undo_redo
import utilities

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
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.file_dropped = ""
        self.table.setRowCount(0)  # Set the initial row count to 0
        self.table.setColumnCount(5)  # Set the column count to 5
        self.setAcceptDrops(True)
        self.undo_ctrlr: undo_redo.UndoRedo = undo_redo.UndoRedo.get_instance()

        # List containing indices of all diff rows. This is used for jump to diff functions
        self.diff_indices: list = []
        self.diff_index_block_end: list = []
        # Contains the index of the current diff that has been jumped to
        self.curr_diff_idx: int = -1
        self.selected_block: list = [0, 0]
        self.block_undo_size: list = []
        self.block_redo_size: list = []

        self.table.cellClicked.connect(self.cellClickedEvent)
        
        self.change_set_a = change_set_a
        self.change_set_b = change_set_b
        self.left_file: str = ""
        self.right_file: str = ""

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
        # gui_cgf.converted ensures test software can run correctly
        if not gui_cfg.converted:
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

            for url in event.mimeData().urls():
                path = url.toLocalFile()

            if self.file_dropped == "":
                self.file_dropped = path
            else:
                self.clear_table()
                fileB = path

                if not utilities.file_writable(self.file_dropped):            
                    QMessageBox.about(self, "Warning ", os.path.basename(self.file_dropped) + " is read only")
                if not utilities.file_writable(fileB):            
                    QMessageBox.about(self, "Warning ", os.path.basename(fileB) + " is read only")

                # I use a local instance of fileIO to generate changesets, since
                # main_table can't access the main window instance of fileIO
                self.file_io = file_io.FileIO()
                result = self.file_io.diff_files(self.file_dropped, fileB)
                if result == pymerge_enums.RESULT.GOOD:
                    result = result = self.file_io.get_change_sets(self.file_io.changes_a, self.file_io.changes_b)

                # I point the local changeSets to a local changeSet
                # but I must point the local changeSets back at the mainWindow changeSets
                # so I user could open different file via file open after they do a click and drag
                change_set_rereference_a = self.change_set_a
                change_set_rereference_b = self.change_set_b
                self.change_set_a = self.file_io.changes_a
                self.change_set_b = self.file_io.changes_b

                self.load_table_contents(self.file_dropped, fileB)

                self.change_set_a = change_set_rereference_a
                self.change_set_b = change_set_rereference_b
                
                self.file_dropped = ""
            
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
        
        self.select_block()
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

        self.select_block()
        self.table.repaint()
        return

    @pyqtSlot()
    def undo_last_change(self):
        """
        undoes last change or group of changes
        :return: No return value
        """
        undo_stack_size = 0
        for n in self.block_undo_size:
            undo_stack_size += n
        
        difference = self.undo_ctrlr.undo_buf_size - undo_stack_size
        for i in range(difference):            
            self.block_undo_size.append(1)
        
        if len(self.block_undo_size) != 0:
            n = self.block_undo_size.pop()
            self.block_redo_size.append(n)
            for i in range(n):            
                self.undo_ctrlr.undo()
                self.undo_ctrlr.undo_buf_size -= 1
        else:
            self.undo_ctrlr.undo()
            if self.undo_ctrlr.undo_buf_size != 0:
                self.undo_ctrlr.undo_buf_size -= 1
        for row in self.rows:
            row.set_row_state()

    @pyqtSlot()
    def redo_last_undo(self):
        """
        redo last undo performed
        :return: No return value
        """
        if len(self.block_redo_size) != 0:
            n = self.block_redo_size.pop()
            self.block_undo_size.append(n)
            for i in range(n):
                self.undo_ctrlr.redo()
        else:
            self.undo_ctrlr.redo()
        for row in self.rows:
            row.set_row_state()

    @pyqtSlot()
    def merge_left(self):
        """
        merge the whole left selection into the right
        """
        
        self.table.clearSelection()
        for n in range(self.selected_block[0], self.selected_block[1]):
            self.rows[n].merge_left()
        
        self.block_undo_size.append(self.selected_block[1] - self.selected_block[0])
                
        undo_stack_size = 0
        for n in self.block_undo_size:
            undo_stack_size += n
        
        difference = undo_stack_size - self.undo_ctrlr.undo_buf_size
        difference = abs(difference)
        for i in range(difference):
            self.block_undo_size.insert( len(self.block_undo_size)-1, 1)

        return

    @pyqtSlot()
    def merge_right(self):
        """
        merge the whole right selection into the left
        """
        self.table.clearSelection()
        for n in range(self.selected_block[0], self.selected_block[1]):
            self.rows[n].merge_right()

        self.block_undo_size.append(self.selected_block[1] - self.selected_block[0])
        
        undo_stack_size = 0
        for n in self.block_undo_size:
            undo_stack_size += n

        difference = undo_stack_size - self.undo_ctrlr.undo_buf_size
        difference = abs(difference)
        for i in range(difference):
            self.block_undo_size.insert( len(self.block_undo_size)-1, 1)
        
        return

    def jump_to_line(self, line_num, col=0):
        self.table.clearSelection()
        self.table.scrollToItem(
            self.table.item(line_num-1, col), QtWidgets.QAbstractItemView.PositionAtTop
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
        :param right_line_num:
        :param left_line_num:
        :param right_text: Right text to display
        :param left_text: Left text to display
        :param line_num: Line number to display. This isn't exactly where it's inserted, just a display value
        :param change_flags:
        :return: No return value

        """
        self.table.insertRow(line_num)
        self.table.setRowHeight(line_num, 28)
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
        row_instance.actual_indices[0] = left_line_num
        row_instance.actual_indices[1] = right_line_num
        
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
        del self.change_set_a.change_list[:]
        del self.change_set_b.change_list[:]
        self.block_undo_size.clear()
        self.block_redo_size.clear()
        self.curr_diff_idx = -1
        self.selected_block[0] = 0
        self.selected_block[1] = 0
        self.diff_indices.clear()
        self.diff_index_block_end.clear()
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
        for n in range(len(self.change_set_a.change_list) - 1):
            data_a = [""]
            data_b = [""]
            change_type_a = [pymerge_enums.CHANGEDENUM.SAME]
            change_type_b = [pymerge_enums.CHANGEDENUM.SAME]
            self.change_set_a.get_change(n, change_type_a, data_a)
            self.change_set_b.get_change(n, change_type_b, data_b)

            self.add_line(data_a[0], data_b[0], n, [change_type_a[0], change_type_b[0]])

        # generate list of diff lines, to enable prev/next diff jump buttons
        n = 0
        while n < len(self.change_set_a.change_list) - 1:
            data_a = [""]
            change_type_a = [pymerge_enums.CHANGEDENUM.SAME]
            self.change_set_a.get_change(n, change_type_a, data_a)
            if change_type_a[0] != pymerge_enums.CHANGEDENUM.SAME:
                self.diff_indices.append(n)
                while change_type_a[0] != pymerge_enums.CHANGEDENUM.SAME:
                    n += 1
                    self.change_set_a.get_change(n, change_type_a, data_a)
                self.diff_index_block_end.append(n)
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

    def select_block(self, n=-1):

        if n != -1:
            j = 0
            for i in self.diff_indices:
                if n >= i:
                   self.curr_diff_idx = j 
                j += 1

        self.table.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.table.clearSelection()
        self.selected_block[0] = self.diff_indices[self.curr_diff_idx]
        self.selected_block[1] = self.diff_index_block_end[self.curr_diff_idx]
        for n in range(self.diff_indices[self.curr_diff_idx], self.diff_index_block_end[self.curr_diff_idx]):
            self.table.selectRow(n)

        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    @pyqtSlot()
    def cellClickedEvent(self):
        if self.rows[self.table.currentRow()].change_state_flags[0] == pymerge_enums.CHANGEDENUM.SAME:
            self.table.clearSelection()
        else:
            self.select_block(self.table.currentRow())
        
 
 
 
 
