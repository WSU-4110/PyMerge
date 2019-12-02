"""
###########################################################################
File: dependency_chk.py
Author:
Description: Checks if certain packages are installed on user's computer. If not,
            it attempts to install missing packages.


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

import subprocess
import sys


def check():
    try:
        import PyQt5
        print("PyQt5 dependency satisfied.")
    except ImportError:
        print("Couldn't find PyQt5 dependency, attempting to install...")
        install("PyQt5")
    try:
        import Cython
        print("Cython dependency satisfied.")
    except ImportError:
        print("Couldn't find Cython dependency, attempting to install...")
        install("Cython")


def install(package):
    try:
        subprocess.call([sys.executable, "-m", "pip", "install", package])
    except:
        print(f"There was an error trying to install {package}")