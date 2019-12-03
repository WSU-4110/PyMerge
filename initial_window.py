"""
###########################################################################
File: initial_window.py
Author:
Description: Window that appears immediately after PyMerge opens. Appears before
            the comparison window.


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

import sys

from PyQt5.QtWidgets import *


class InitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Initial Window")
        self.setGeometry(1000, 1000, 2000, 1000)


def start_window():
    app = QApplication(sys.argv)
    ex = InitialWindow()


