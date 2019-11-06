# PyQt imports
# Standard imports
from copy import deepcopy

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)

# Project imports
import gui_config as gui_cfg
import pmEnums
import undo_redo


class Row(QtCore.QObject):
    # __slots__ = [
    #     "row",
    #     "table",
    #     "right_text",
    #     "left_text",
    #     "line_num",
    #     "change_state_flags",
    #     "deleted",
    #     "actual_indices",
    #     "right_button",
    #     "left_button",
    #     "undo_ctrlr"
    # ]

    def __init__(
        self,
        row: int,
        table: QTableWidget,
        right_text: str or None,
        left_text: str or None,
        line_num: int,
        change_flags: list,
    ):
        """
        Initialize the Row class instance
        :param row: row number
        :param table: table widget instance
        :param right_text: string containing the right side text
        :param left_text: string containg the left side text
        :param line_num:
        """
        super().__init__()
        self.row_num: int = row
        self.table: QTableWidget = table
        self.right_text: str = right_text
        self.left_text: str = left_text
        self.line_num: int = line_num
        self.right_background_color = None
        self.left_background_color = None
        self.change_state_flags = deepcopy(change_flags)
        self.row_deleted: list = [False, False]  # Indicates if either side was deleted.
        self.right_button = None
        self.left_button = None
        self.actual_indices = [-1, -1]    # Actual line numbers in the files
        self.undo_ctrlr = undo_redo.UndoRedo.get_instance()

        # Set the left and right background colors
        if self.change_state_flags[0] == pmEnums.CHANGEDENUM.CHANGED:
            self.set_left_background(gui_cfg.COLORS["ROW_DIFF"], buttons=True)

        elif self.change_state_flags[1] == pmEnums.CHANGEDENUM.PADDING:
            self.set_left_background(gui_cfg.COLORS["ROW_PAD_SPACE"], buttons=True)

        elif self.change_state_flags[0] == pmEnums.CHANGEDENUM.ADDED:
            self.set_left_background(gui_cfg.COLORS["ROW_PAD_SPACE"], buttons=True)

        elif self.change_state_flags[0] == pmEnums.CHANGEDENUM.SAME:
            self.set_left_background(gui_cfg.COLORS["ROW_DEFAULT"])
            #self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        if self.change_state_flags[1] == pmEnums.CHANGEDENUM.CHANGED:
            self.set_right_background(gui_cfg.COLORS["ROW_DIFF"], buttons=True)

        elif self.change_state_flags[1] == pmEnums.CHANGEDENUM.PADDING:
            self.set_right_background(gui_cfg.COLORS["ROW_PAD_SPACE"], buttons=True)

        elif self.change_state_flags[1] == pmEnums.CHANGEDENUM.ADDED:
            self.set_right_background(gui_cfg.COLORS["ROW_PAD_SPACE"], buttons=True)
            
        elif self.change_state_flags[1] == pmEnums.CHANGEDENUM.SAME:
            self.set_right_background(gui_cfg.COLORS["ROW_DEFAULT"])
            #self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

    def set_right_background(self, background, buttons=False):
        #self.table.item(self.row_num, gui_cfg.RIGHT_TXT_COL_IDX).setFlags(QtCore.Qt.ItemIsEditable)
        self.table.item(self.row_num, gui_cfg.RIGHT_TXT_COL_IDX).setBackground(
            background
        )
        self.right_background_color = background
        if buttons:
            self.add_row_merge_buttons()
        self.table.repaint()

    def set_left_background(self, background, buttons=False):
        self.table.item(self.row_num, gui_cfg.LEFT_TXT_COL_IDX).setBackground(
            background
        )
        self.left_background_color = background
        if buttons:
            self.add_row_merge_buttons()
        self.table.repaint()

    def add_row_merge_buttons(self):
        self.right_button = QPushButton(self.table)
        self.right_button.setIcon(gui_cfg.ICONS["MERGE_RIGHT"])
        self.right_button.clicked.connect(self.merge_right)
        self.right_button.setMaximumSize(60, 40)
        self.table.setCellWidget(self.line_num, 2, self.right_button)

        self.left_button = QPushButton(self.table)
        self.left_button.setIcon(gui_cfg.ICONS["MERGE_LEFT"])
        self.left_button.clicked.connect(self.merge_left)
        self.left_button.setMaximumSize(60, 40)
        self.table.setCellWidget(self.line_num, 3, self.left_button)
        return

    @pyqtSlot()
    def merge_right(self):
        """
        Merge lines from the right to the left
        :return: No return value
        """
        # This is a significant user action so we need to record the change in the undo stack
        self.undo_ctrlr.record_action(self)

        # Set booleans
        if self.change_state_flags[1] == pmEnums.CHANGEDENUM.ADDED:
            self.row_deleted[0] = True
            self.row_deleted[1] = True

        # Copy the left text to the right side
        self.table.setItem(
            self.row_num, gui_cfg.LEFT_TXT_COL_IDX, QTableWidgetItem(self.left_text)
        )

        # Set the background colors accordingly. We need a change flag to determine the color to use
        self.table.item(self.row_num, gui_cfg.LEFT_TXT_COL_IDX).setBackground(
            gui_cfg.COLORS["ROW_MERGED"]
        )
        self.table.item(self.row_num, gui_cfg.RIGHT_TXT_COL_IDX).setBackground(
            gui_cfg.COLORS["ROW_MERGED"]
        )

        self.left_background_color = gui_cfg.COLORS["ROW_MERGED"]
        self.right_background_color = gui_cfg.COLORS["ROW_MERGED"]
        self.right_text = self.left_text

        # Table isn't gonna repaint itself. Gotta show users the changes we just made.
        self.table.repaint()

    @pyqtSlot()
    def merge_left(self):
        """
        Merge lines from the left to the right
        :return: No return value
        """
        # This is a significant user action so we need to record the change in the undo stack
        self.undo_ctrlr.record_action(self)

        # Set booleans
        if self.change_state_flags[0] == pmEnums.CHANGEDENUM.ADDED:
            self.row_deleted[0] = True
            self.row_deleted[1] = True

        # Copy the right text to the right side
        self.table.setItem(
            self.row_num, gui_cfg.RIGHT_TXT_COL_IDX, QTableWidgetItem(self.right_text)
        )

        # Set the background colors accordingly. We need a change flag to determine the color to use
        self.table.item(self.row_num, gui_cfg.LEFT_TXT_COL_IDX).setBackground(
            gui_cfg.COLORS["ROW_MERGED"]
        )
        self.table.item(self.row_num, gui_cfg.RIGHT_TXT_COL_IDX).setBackground(
            gui_cfg.COLORS["ROW_MERGED"]
        )
        self.left_background_color = gui_cfg.COLORS["ROW_MERGED"]
        self.right_background_color = gui_cfg.COLORS["ROW_MERGED"]
        self.left_text = self.right_text

        # Table isn't gonna repaint itself. Gotta show users the changes we just made.
        self.table.repaint()

    def set_row_state(self):
        self.table.setItem(
            self.row_num, gui_cfg.LEFT_TXT_COL_IDX, QTableWidgetItem(self.right_text)
        )
        self.table.setItem(
            self.row_num, gui_cfg.RIGHT_TXT_COL_IDX, QTableWidgetItem(self.left_text)
        )

        self.table.item(self.row_num, gui_cfg.RIGHT_TXT_COL_IDX).setBackground(
            self.right_background_color
        )
        self.table.item(self.row_num, gui_cfg.LEFT_TXT_COL_IDX).setBackground(
            self.left_background_color
        )

        self.table.repaint()

