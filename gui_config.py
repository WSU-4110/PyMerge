"""
Configurations and globals for GUI
"""

from PyQt5.QtGui import QFont, QColor

"""
Icon paths 
"""
ICONS = {
    "MERGE_RIGHT": "icons/left-arrow.png",
    "MERGE_LEFT": "icons/right-arrow.png",
    "UNDO": "icons/undo-arrow.png",
    "REDO": "icons/redo-arrow.png",
    "ADD_FILE": "icons/add.png",
    "PREV_DIFF": "icons/up-arrow.png",
    "NEXT_DIFF": "icons/down-arrow.png",
}


"""
Colors to be used for all styling the GUI. 
Each dictionary object should be an instance of the QColor class
"""
COLORS = {
    "LINE_DIFF": QColor(255, 150, 150),
    "LINE_MERGE": QColor(219, 235, 255),
    "PAD_SPACE": QColor(240, 240, 240),
    "DEFAULT": QColor(255, 255, 255),
    "TBL_HEADER_DEFAULT_BACKGROUND": QColor(179, 179, 179),
    "TBL_HEADER_DEFAULT_FOREGROUND": QColor(0, 0, 0),
    "TBL_LINE_COL_DEFAULT_BACKGROUND": QColor(242, 242, 242)
}

"""
Fonts to be used throughout the GUI
"""
FONTS = {
    "TBL_HEADER_DEFAULT": QFont("Open Sans Bold", weight=QFont.Bold, pointSize=12),
    "TOOLBAR_DEFAULT": QFont("Open Sans Bold", weight=QFont.Bold),
}
