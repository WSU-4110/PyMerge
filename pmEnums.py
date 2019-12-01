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
various enumerations, to standardize the output and input that functions 
are expecting to get. 
"""
from enum import Enum


class RESULT(Enum):
    GOOD = 0
    ERROR = 1
    NOTIMPL = 2  # not implemented
    BADFILE = 3  # file mismatch
    EMPTYFILE = 4


class ATTRIB(Enum):
    DATA = 0
    CHANGE = 1


class CHANGEDENUM(Enum):
    SAME = 0
    CHANGED = 1
    ADDED = 2
    MOVED = 3
    PADDING = 4
    ERROR = 5
