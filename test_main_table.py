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

import sys
import unittest

from PyQt5.QtWidgets import QApplication

import main_window

app = QApplication(sys.argv)


class TestMainTable(unittest.TestCase):
    def setUp(self):
        self.mainWindow = main_window.MainWindow("file1.c", "file2.c")
        self.table = self.mainWindow.table_widget
        # for testing button presses on window with no input files
        self.mainWindow2 = main_window.MainWindow()
        self.table2 = self.mainWindow2.table_widget
        
    def test_goto_next_diff(self):        
        self.table.goto_next_diff()
        self.table.goto_next_diff()                
        expectedDiffIndex = 1
        self.assertEqual(expectedDiffIndex, self.table.curr_diff_idx)
        expectedDiffLine = 9
        self.assertEqual(expectedDiffLine, self.table.table.currentRow())

        # an empty table will leave the curr_diff_indx at -1
        self.table2.goto_next_diff()
        self.assertEqual(-1, self.table2.curr_diff_idx)

    def test_goto_prev_diff(self):
        self.table.goto_next_diff()
        self.table.goto_next_diff()
        self.table.goto_next_diff()
        self.table.goto_prev_diff()

        """
        go down two diffs, then back one, you should be at the top diff.
        Go back another diff and you will be wrapped around to the last diff
        """
        expectedDiffIndex = 1
        self.assertEqual( expectedDiffIndex, self.table.curr_diff_idx  )
        expectedDiffLine = 9
        self.assertEqual( expectedDiffLine, self.table.table.currentRow() )

        self.table.goto_prev_diff()
        self.table.goto_prev_diff()
        expectedLastIndex = 8
        self.assertEqual( expectedLastIndex, self.table.curr_diff_idx  )
        expectedLastDiffLine = 58
        self.assertEqual( expectedLastDiffLine, self.table.table.currentRow() )        
        
        #empty tables index should be left at -1 when prev is hit.
        self.table2.goto_prev_diff()
        self.assertEqual( -1, self.table2.curr_diff_idx)

    def test_merge_left(self):
        self.table.goto_next_diff()
        self.table.goto_next_diff()

        self.table.merge_left()
        expectedLineNine = ""
        expectedLineTen = "typedef structtypedef"
        
        self.assertEqual( expectedLineNine, self.table.rows[8].left_text)
        self.assertEqual( expectedLineNine, self.table.rows[8].right_text)
        self.assertEqual( expectedLineTen, self.table.rows[9].left_text)
        self.assertEqual( expectedLineTen, self.table.rows[9].right_text)

    def test_merge_right(self):
        self.table.goto_next_diff()
        self.table.goto_next_diff()

        self.table.merge_right()
        expectedLineTen = ""
        expectedLineNine = "typedef structtypedefC"
        
        self.assertEqual( expectedLineNine, self.table.rows[8].left_text)
        self.assertEqual( expectedLineNine, self.table.rows[8].right_text)
        self.assertEqual( expectedLineTen, self.table.rows[9].left_text)
        self.assertEqual( expectedLineTen, self.table.rows[9].right_text)

    def test_undo(self):
        self.table.goto_next_diff()
        self.table.goto_next_diff()

        self.table.merge_right()
        self.table.undo_last_change()

        self.assertNotEqual(self.table.rows[8].left_text, self.table.rows[8].right_text)
        self.assertNotEqual(self.table.rows[9].left_text, self.table.rows[9].right_text)        
        
    def test_redo(self):
        self.table.goto_next_diff()
        self.table.goto_next_diff()

        self.table.merge_right()
        self.table.undo_last_change()
        self.table.redo_last_undo()

        self.assertEqual(self.table.rows[8].left_text, self.table.rows[8].right_text)
        self.assertEqual(self.table.rows[9].left_text, self.table.rows[9].right_text)

            
if __name__ == '__main__':
    unittest.main()
