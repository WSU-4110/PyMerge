"""
###########################################################################
File: changeset.py
Author:
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

"""
class, provides a data structure to make working with file differences (change sets)
easier by abstracting the data storage, and providing a single accessor function.
"""

import pymerge_enums


class ChangeSet(object):

	def __init__(self):
		self.change_list: list = []
		self.change_set_ready: bool = False

	def get_change(self, line_num, change_type, data):
		change = self.change_list[line_num]
		change_type[0] = change[1]
		data[0] = change[2]
		return pymerge_enums.RESULT.NOTIMPL

	def add_change(self, line_num, change_type, data):
		self.change_list.append((line_num, change_type, data))
