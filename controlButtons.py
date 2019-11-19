"""
Widget to contain the buttons/control panel for the merge tool. 
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import PyQt5
import gui_config


class controlButtons(QWidget):
    def __init__(self, tableObj, mainTableObj):

        self.tableObj = tableObj
        self.mainTableObj = mainTableObj
        super().__init__()
        self.setGeometry(200, 200, 200, 200)
        self.buttonLayout()


    def buttonLayout(self):
        grid = QGridLayout()
        self.setLayout(grid)

        import_file1_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["IMPORT_FILE"])
        import_file1_button.setIcon(icon)
        import_file1_button.setFixedHeight(50)
        import_file1_button.setToolTip("import left file")
        import_file1_button.clicked.connect(self.mainTableObj.import_file1)
        grid.addWidget(import_file1_button, 1, 0)

        merge_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["MERGE"])
        merge_button.setIcon(icon)
        merge_button.setFixedWidth(50)
        merge_button.setToolTip("merge files")
        merge_button.clicked.connect(self.mainTableObj.merge_files)
        grid.addWidget(merge_button, 1, 2)

        import_file2_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["IMPORT_FILE"])
        import_file2_button.setIcon(icon)
        import_file2_button.setFixedHeight(50)
        import_file2_button.setToolTip("import right file")
        import_file2_button.clicked.connect(self.mainTableObj.import_file2)
        grid.addWidget(import_file2_button, 1, 5)

        merge_left_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["MERGE_LEFT"])
        merge_left_button.setIcon(icon)
        merge_left_button.setFixedHeight(50)
        merge_left_button.setToolTip('merge left version into right')
        merge_left_button.clicked.connect(self.tableObj.merge_left)
        grid.addWidget(merge_left_button, 0, 0)

        undo_change_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["UNDO"])
        undo_change_button.setIcon(icon)
        undo_change_button.setFixedHeight(50)
        undo_change_button.setToolTip("undo last merge")
        undo_change_button.clicked.connect(self.tableObj.undo_last_change)
        grid.addWidget(undo_change_button, 0, 1)
        
        next_diff_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["NEXT_DIFF"])
        next_diff_button.setIcon(icon)
        next_diff_button.setFixedHeight(50)
        next_diff_button.setToolTip("goto next difference")
        next_diff_button.clicked.connect(self.tableObj.goto_next_diff)
        grid.addWidget(next_diff_button, 0, 2)
        
        prev_diff_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["PREV_DIFF"])
        prev_diff_button.setIcon(icon)
        prev_diff_button.setFixedHeight(50)
        prev_diff_button.setToolTip("goto previous difference")
        prev_diff_button.clicked.connect(self.tableObj.goto_prev_diff)
        grid.addWidget(prev_diff_button, 0, 3)

        redo_change_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["REDO"])
        redo_change_button.setIcon(icon)
        redo_change_button.setFixedHeight(50)
        redo_change_button.setToolTip("redo last change")
        redo_change_button.clicked.connect(self.tableObj.redo_last_undo)
        grid.addWidget(redo_change_button, 0, 4)
        
        merge_right_button = QPushButton()
        icon = QtGui.QIcon(gui_config.ICONS["MERGE_RIGHT"])
        merge_right_button.setIcon(icon)
        merge_right_button.setFixedHeight(50)
        merge_right_button.setToolTip("merge right version into left")
        merge_right_button.clicked.connect(self.tableObj.merge_right)
        grid.addWidget(merge_right_button, 0, 5)
