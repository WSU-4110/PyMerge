"""
Configurations and globals for GUI
"""

from PyQt5.QtGui import QFont, QColor, QIcon

"""
This file contains global configurations for PyMerge regarding color, icons, and text.
The configurations in this file are not and should not influence structural aspects of the PyMerge
GUI.

Acceptable additions to gui_config.py:
    - Icons: paths and QIcon objects
    - Colors: background colors, foreground colors, text colors, etc. These will ideally be QColor objects.
    - Fonts: These should be QFont objects so new class instances are created all over the place.
    - Table column indices: Since the headers and data for the main table need to be matched, setting the indices
        globally is desireable.
"""



"""
Icon paths

These are set as paths to begin with, then converted to QIcon instances once the main application is created.
This is due to PyQt5 restrictions. The naming convention for constants is used here even though
the dictionary items are changed because this change is only done to get around PyQt5 instantiation 
restrictions on the QIcon class. After the conversion from a raw path to a QIcon object is done, 
these item are not changed for the rest of the runtime of the program.
"""
ICONS = {
    "OBJ_CONVERSION": [False],
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

BG = Background color
FG = Foreground color
"""
COLORS = {
    "ROW_DIFF": QColor(255, 150, 150),
    "ROW_MERGED": QColor(219, 235, 255),
    "ROW_PAD_SPACE": QColor(82, 82, 82),
    "ROW_DEFAULT": QColor(237, 255, 240),
    "ROW_ACTV_BG": QColor(31, 98, 255),
    "ROW_ACTV_TXT": QColor(0, 0, 0),
    "ROW_INACTV_BG": QColor(237, 255, 240),
    "ROW_INACTV_TXT": QColor(0, 0, 0),
    "TBL_HDR_DEFAULT_BG": QColor(179, 179, 179),
    "TBL_HDR_DEFAULT_FG": QColor(0, 0, 0),
    "TBL_LINE_COL_DEFAULT_BG": QColor(242, 242, 242)
}

"""
Fonts to be used throughout the GUI
"""
FONTS = {
    "TBL_HEADER_DEFAULT": QFont("Open Sans Bold", weight=QFont.Bold, pointSize=12),
    "TOOLBAR_DEFAULT": QFont("Open Sans Bold", weight=QFont.Bold),
}

LEFT_TXT_COL_IDX = 1
RIGHT_TXT_COL_IDX = 4


def convert_icon_dict():
    global ICONS

    if not ICONS["OBJ_CONVERSION"][0]:
        for icon in ICONS:
            if isinstance(ICONS[icon], str):
                ICONS[icon] = QIcon(ICONS[icon])
        ICONS["OBJ_CONVERSION"][0] = True
        ICONS["OBJ_CONVERSION"] = set(ICONS["OBJ_CONVERSION"])

