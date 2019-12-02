"""
###########################################################################
File: file_io.py
Author:
Description: An input/output interface for user selected files.


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

"""
fileIO class, providing an interface for the GUI to input files, and get changeSets. After the GUI has two
changeSet objects, it is able to handle the rest of the application requirements on its
own untill it is time to write changes. 
"""

import ntpath

import changeset
import diff_resolution
import pymerge_enums
import utilities

import os
import os.path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

class FileIO(object):
    def __init__(self):
        self.changes_b = changeset.ChangeSet()
        self.changes_a = changeset.ChangeSet()

    def diff_files(self, file_a, file_b):

        if file_a == "" or file_b == "":
            return pymerge_enums.RESULT.EMPTYFILE

        file_a_base_name = ntpath.basename(file_a)
        file_b_base_name = ntpath.basename(file_b)

        if not utilities.valid_file_ext(file_a):
            print("\n[-] Unacceptable file type:", file_a_base_name, "\n")
            return pymerge_enums.RESULT.BADFILE

        if not utilities.valid_file_ext(file_b):
            print("\n[-] Unacceptable file type:", file_b_base_name, "\n")
            return pymerge_enums.RESULT.BADFILE

        file_a_open = open(file_a, "r")
        file_b_open = open(file_b, "r")

        result = diff_resolution.diff_set(
            file_a_open, file_b_open, file_a_open, file_b_open, self.changes_a, self.changes_b
        )

        file_a_open.close()
        file_b_open.close()

        if result == pymerge_enums.RESULT.GOOD:
            if not utilities.file_writable(file_a):            
                return pymerge_enums.RESULT.READONLYA

            if not utilities.file_writable(file_b):
                return pymerge_enums.RESULT.READONLYB

            return pymerge_enums.RESULT.GOOD


    def get_change_sets(self, file_a, file_b):
        file_a = self.changes_a
        file_b = self.changes_b
        if self.changes_a != 0 and self.changes_b != 0:
            return pymerge_enums.RESULT.GOOD
        return pymerge_enums.RESULT.ERROR
