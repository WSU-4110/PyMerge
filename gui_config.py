"""
Configurations and globals for GUI
"""

from PyQt5 import QtGui

ICONS = {
    "MERGE_RIGHT": "icons/left-arrow.png",
    "MERGE_LEFT": "icons/right-arrow.png",
    "UNDO": "icons/undo-arrow.png",
    "REDO": "icons/redo-arrow.png",
    "ADD_FILE": "icons/add.png",
}

COLORS = {
    "LINE_DIFF": QtGui.QColor(255, 150, 150),
    "LINE_MERGE": QtGui.QColor(219, 235, 255),
    "PAD_SPACE": QtGui.QColor(240, 240, 240),
    "DEFAULT": QtGui.QColor(255, 255, 255)
}