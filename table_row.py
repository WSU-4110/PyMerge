# PyQt imports
from PyQt5.QtWidgets import (
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

# Standard imports
from copy import deepcopy

# Project imports
import gui_config as gui_cfg
import undo_redo
import pmEnums

undo_ctrlr = undo_redo.UndoRedo.get_instance()


class Row(QtCore.QObject):
    __slots__ = [
        "row",
        "table",
        "right_text",
        "left_text",
        "line_num",
        "change_state_flags",
        "deleted"
        "right_button",
        "left_button",
    ]

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
        self.row_deleted: list = [False, False] # Indicates if either side was deleted.
        self.right_button = None
        self.left_button = None

        # Set the left side background colors
        if self.change_state_flags[0] == pmEnums.CHANGEDENUM.CHANGED:
            self.table.item(self.row_num, gui_cfg.LEFT_TXT_COL_IDX).setBackground(
                gui_cfg.COLORS["ROW_DIFF"]
            )
            self.add_row_merge_buttons()

        elif self.change_state_flags[1] == pmEnums.CHANGEDENUM.PADDING:
            self.table.item(self.row_num, gui_cfg.LEFT_TXT_COL_IDX).setBackground(
                gui_cfg.COLORS["ROW_PAD_SPACE"]
            )
            self.add_row_merge_buttons()

        elif self.change_state_flags[0] == pmEnums.CHANGEDENUM.ADDED:
            self.table.item(self.row_num, gui_cfg.LEFT_TXT_COL_IDX).setBackground(
                gui_cfg.COLORS["ROW_PAD_SPACE"]
            )
            self.add_row_merge_buttons()

        elif self.change_state_flags[0] == pmEnums.CHANGEDENUM.SAME:
            self.table.item(self.row_num, gui_cfg.LEFT_TXT_COL_IDX).setBackground(
                gui_cfg.COLORS["ROW_DEFAULT"]
            )

        # Set the right side background colors
        if self.change_state_flags[1] == pmEnums.CHANGEDENUM.CHANGED:
            self.table.item(self.row_num, gui_cfg.RIGHT_TXT_COL_IDX).setBackground(
                gui_cfg.COLORS["ROW_DIFF"]
            )
            self.add_row_merge_buttons()

        elif self.change_state_flags[1] == pmEnums.CHANGEDENUM.PADDING:
            self.table.item(self.row_num, gui_cfg.RIGHT_TXT_COL_IDX).setBackground(
                gui_cfg.COLORS["ROW_PAD_SPACE"]
            )
            self.add_row_merge_buttons()

        elif self.change_state_flags[1] == pmEnums.CHANGEDENUM.ADDED:
            self.table.item(self.row_num, gui_cfg.RIGHT_TXT_COL_IDX).setBackground(
                gui_cfg.COLORS["ROW_PAD_SPACE"]
            )
            self.add_row_merge_buttons()

        elif self.change_state_flags[1] == pmEnums.CHANGEDENUM.SAME:
            self.table.item(self.row_num, gui_cfg.RIGHT_TXT_COL_IDX).setBackground(
                gui_cfg.COLORS["ROW_DEFAULT"]
            )

        self.table.repaint()

    def add_row_merge_buttons(self):
        self.right_button = QPushButton(self.table)
        self.right_button.setIcon(gui_cfg.ICONS["MERGE_RIGHT"])
        self.right_button.clicked.connect(self.merge_right)
        self.table.setCellWidget(self.line_num, 2, self.right_button)

        self.left_button = QPushButton(self.table)
        self.left_button.setIcon(gui_cfg.ICONS["MERGE_LEFT"])
        self.left_button.clicked.connect(self.merge_left)
        self.table.setCellWidget(self.line_num, 3, self.left_button)

    @pyqtSlot()
    def merge_right(self):
        """
        Merge lines from the right to the left
        :return: No return value
        """
        print(self.change_state_flags)
        # Set booleans
        if self.change_state_flags[1] == pmEnums.CHANGEDENUM.ADDED:
            self.row_deleted[0] = True
            self.row_deleted[1] = True

        # Copy the left text to the right side
        self.table.setItem(
            self.row_num, gui_cfg.LEFT_TXT_COL_IDX, QTableWidgetItem(self.left_text)
        )
        self.right_text = self.left_text

        # Set the background colors accordingly. We need a change flag to determine the color to use
        self.table.item(self.row_num, gui_cfg.LEFT_TXT_COL_IDX).setBackground(
            gui_cfg.COLORS["ROW_MERGED"]
        )
        self.table.item(self.row_num, gui_cfg.RIGHT_TXT_COL_IDX).setBackground(
            gui_cfg.COLORS["ROW_MERGED"]
        )

        # This is a significant user action so we need to record the change in the undo stack
        #undo_ctrlr.record_action(self)

        # Table isn't gonna repaint itself. Gotta show users the changes we just made.
        self.table.repaint()

    @pyqtSlot()
    def merge_left(self):
        """
        Merge lines from the left to the right
        :return: No return value
        """
        # Set booleans
        if self.change_state_flags[0] == pmEnums.CHANGEDENUM.ADDED:
            self.row_deleted[0] = True
            self.row_deleted[1] = True

        # Copy the right text to the right side
        self.table.setItem(
            self.row_num, gui_cfg.RIGHT_TXT_COL_IDX, QTableWidgetItem(self.right_text)
        )
        self.left_text = self.right_text

        # Set the background colors accordingly. We need a change flag to determine the color to use
        self.table.item(self.row_num, gui_cfg.LEFT_TXT_COL_IDX).setBackground(
            gui_cfg.COLORS["ROW_MERGED"]
        )
        self.table.item(self.row_num, gui_cfg.RIGHT_TXT_COL_IDX).setBackground(
            gui_cfg.COLORS["ROW_MERGED"]
        )

        # This is a significant user action so we need to record the change in the undo stack
        #undo_ctrlr.record_action(self)

        # Table isn't gonna repaint itself. Gotta show users the changes we just made.
        self.table.repaint()
