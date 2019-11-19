
import unittest
import mainWindow
import sys

from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

class TestMainTable(unittest.TestCase):

    
    def setUp(self):
        self.mainWindow = mainWindow.mainWindow("file1.c", "file2.c")
        self.table = self.mainWindow.table_widget
        
    def test_goto_next_diff(self):
        self.table.goto_next_diff()
        self.table.goto_next_diff()
        input("waiting :)")
        expectedDiffIndex = 8
        self.assertEqual( expectedDiffIndex, self.table.curr_diff_idx  )


if __name__ == '__main__':
    unittest.main()
