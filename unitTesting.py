import unittest
import utilities
import MainWindow
import utilities
import FileIO
import sys
import utilities
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

class UnitTest(unittest.TestCase):

    def setUp(self):
        self.mainWindow = MainWindow.MainWindow("file1.c", "file2.c")
        self.fileIO = FileIO
        self.util = utilities

    def test_openFile(self):
        self.mainWindow.open_file()
        expectedFileA = "/Users/saularraffi/Documents/School Work Archive/Fall " \
                        "2019 Semester/Software Engineering/Lab/PyMerge/file1.c"
        expectedFileB = "/Users/saularraffi/Documents/School Work Archive/Fall " \
                        "2019 Semester/Software Engineering/Lab/PyMerge/file2.c"
        self.assertEqual(self.mainWindow.fileA, expectedFileA)
        self.assertEqual(self.mainWindow.fileB, expectedFileB)

    def test_valid_file_ext(self):
        self.assertEqual(self.util.valid_file_ext("file1.c"), True)
        self.assertEqual(self.util.valid_file_ext("file2.c"), True)
        self.assertEqual(self.util.valid_file_ext("badFile.docx"), False)

    def test_file_readable(self):
        self.assertEqual(self.util.file_readable("file1.c"), True)
        self.assertEqual(self.util.file_readable("file2.c"), True)

    def test_file_writable(self):
        self.assertEqual(self.util.file_writable("file1.c"), True)
        self.assertEqual(self.util.file_writable("file2.c"), True)

    def test_valid_file_size(self):
        self.assertEqual(self.util.validate_file_size("file1.c", 1000), True)
        self.assertEqual(self.util.validate_file_size("file1.c", 900), True)
        self.assertEqual(self.util.validate_file_size("file1.c", 850), True)
        self.assertEqual(self.util.validate_file_size("file1.c", 849), False)

    def test_check_paths(self):
        file1_path = "/Users/saularraffi/Documents/School Work Archive/Fall " \
                        "2019 Semester/Software Engineering/Lab/PyMerge/file1.c"
        file2_path = "/Users/saularraffi/Documents/School Work Archive/Fall " \
                        "2019 Semester/Software Engineering/Lab/PyMerge/file2.c"
        invalid_path = "/Users/saularraffi/Documents/School Work Archive/Fall " \
                        "2019 Semester/Software Engineering/Lab/PyMerge/does-not-exist.txt"
        self.assertEqual(self.util.check_paths(file1_path),True)
        self.assertEqual(self.util.check_paths(file2_path), True)
        self.assertEqual(self.util.check_paths(invalid_path), False)


if __name__ == '__main__':
    unittest.main()
