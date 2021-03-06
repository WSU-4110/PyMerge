"""
###########################################################################
File: file_open_dialog.py
Author:
Description: Creates a dialog box for opening files to load into comparison table.


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

from PyQt5.QtWidgets import QWidget, QFileDialog


class FileOpenDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.file_name = ""
        self.title = 'Open File'
        self.setGeometry(100, 100, 400, 500)
              
    def open_file_name_dialog(self, openWhat):
        options = QFileDialog.Options()
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open " + openWhat, "", "", options=options)

