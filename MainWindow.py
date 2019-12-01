"""
###########################################################################
File:
Author:
Description:


Copyright (C) 2019

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

"""
Main Window
"""

import os
import os.path
import subprocess
import sys
from sys import platform

from PyQt5.QtWidgets import *

import ControlButtons
import FileIO
import FileOpenDialog
import main_table
import pmEnums
import utilities


class MainWindow(QMainWindow, QMessageBox):
    def __init__(self, fileA=0, fileB=0):
        super().__init__()
        self.setWindowTitle("PyMerge")
        self.setGeometry(10, 50, 1750, 900)
        self.table_widget = 0
        self.control_buttons_widget = 0
        layout = QGridLayout()

        self.fileA = ""
        self.fileB = ""

        # load files and generate changesets
        result = pmEnums.RESULT.ERROR
        self.fIO = FileIO.FileIO()
        if fileA != 0 and fileB != 0:
            result = self.fIO.diff_files(fileA, fileB)
            if result == pmEnums.RESULT.GOOD:
                result = self.fIO.get_change_sets(self.fIO.changes_a, self.fIO.changes_b)

        self.table_widget = 0
        # load table
        self.table_widget = main_table.MainTable(self.fIO.changes_a, self.fIO.changes_b)
        # add table

        layout.addWidget(self.table_widget, 1, 0)

        # load table with fileA and B if present from command line
        if fileA != 0 and fileB != 0:
            self.table_widget.load_table_contents(fileA, fileB)  # Left list arguments for now
        self.table_widget.load_table_contents()  # Left list arguments for now
        
        self.control_buttons_widget = ControlButtons.ControlButtons(self.table_widget)
        layout.addWidget(self.control_buttons_widget, 0, 0)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.init_ui()

    def init_ui(self):
        # start GUI

        self.menu_items()
        self.show()

    def open_file(self):

        self.table_widget.clear_table()

        file_opener_a = FileOpenDialog.FileOpenDialog()
        file_opener_b = FileOpenDialog.FileOpenDialog()
        
        file_opener_a.open_file_name_dialog()
        file_a = file_opener_a.file_name
        
        if file_a != "":
            file_opener_b.open_file_name_dialog()
        file_b = file_opener_b.file_name

        if not utilities.file_writable(file_a):
            QMessageBox.about(self, "Error", os.path.basename(file_a) + " is not writable")
            return
        if not utilities.file_writable(file_b):
            QMessageBox.about(self, "Error", os.path.basename(file_b) + " is not writable")
            return
        
        result = self.fIO.diff_files(file_a, file_b)

        if result == pmEnums.RESULT.GOOD:
            result = self.fIO.get_change_sets(self.fIO.changes_a, self.fIO.changes_b)

        elif result == pmEnums.RESULT.BADFILE:
            QMessageBox.about(self, "Error", "Invalid file type")

        self.table_widget.load_table_contents(file_a, file_b)
        return result

    def menu_items(self):
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        # MENUBAR
        # ~~~~~~~~~~~~~~~~~~~~~~~~
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        edit_menu = main_menu.addMenu('Edit')
        view_menu = main_menu.addMenu('View')
        help_menu = main_menu.addMenu('Help')
        
        open_file_button = QAction("Open Files", self)
        open_file_button.setShortcut('Ctrl+o')
        open_file_button.triggered.connect(lambda: self.open_file())
        file_menu.addAction(open_file_button)

        save_file_button = QAction("Save Files", self)
        save_file_button.setShortcut('Ctrl+s')
        save_file_button.triggered.connect(self.table_widget.write_merged_files)
        file_menu.addAction(save_file_button)

        merge_left_btn = QAction("Merge Left", self)
        merge_left_btn.setShortcut('Ctrl+l')
        merge_left_btn.triggered.connect(self.table_widget.merge_left)
        edit_menu.addAction(merge_left_btn)

        merge_right_btn = QAction("Merge Right", self)
        merge_right_btn.setShortcut('Ctrl+r')
        merge_right_btn.triggered.connect(self.table_widget.merge_right)
        edit_menu.addAction(merge_right_btn)

        prev_diff_btn = QAction("Previous Difference", self)
        prev_diff_btn.setShortcut('Ctrl+p')
        prev_diff_btn.triggered.connect(self.table_widget.goto_prev_diff)
        edit_menu.addAction(prev_diff_btn)

        next_diff_btn = QAction("Next Difference", self)
        next_diff_btn.setShortcut('Ctrl+n')
        next_diff_btn.triggered.connect(self.table_widget.goto_next_diff)
        edit_menu.addAction(next_diff_btn)

        undo_change_btn = QAction("Undo", self)
        undo_change_btn.setShortcut('Ctrl+z')
        undo_change_btn.triggered.connect(self.table_widget.undo_last_change)
        edit_menu.addAction(undo_change_btn)

        redo_change_btn = QAction("Redo", self)
        redo_change_btn.setShortcut('Ctrl+y')
        redo_change_btn.triggered.connect(self.table_widget.redo_last_undo)
        edit_menu.addAction(redo_change_btn)

        hide_show_btns = QAction("Hide/Show Buttons", self)
        #no shortcut
        hide_show_btns.triggered.connect(lambda: self.hide_show_btns_func())
        view_menu.addAction(hide_show_btns)

        help_btn = QAction("Manual", self)
        #no shortcut
        help_btn.triggered.connect(lambda: self.open_help())
        help_menu.addAction(help_btn)

    def hide_show_btns_func(self):
        if self.control_buttons_widget.isVisible():
            self.control_buttons_widget.hide()
        else:
            self.control_buttons_widget.show()

    @staticmethod
    def open_help():
        if platform == "win32":            
            subprocess.Popen("PyMerge_Manual.pdf",shell=True)
        else:
            subprocess.Popen("open PyMerge_Manual.pdf",shell=True)


def start_main(fileA=0, fileB=0):
    app = QApplication(sys.argv)
    ex = MainWindow(fileA, fileB)
    sys.exit(app.exec_())

