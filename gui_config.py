"""
Configurations and globals for GUI
"""

from PyQt5 import QtGui

"""
Icon paths 
"""
ICONS = {
    "MERGE_RIGHT": "icons/left-arrow.png",
    "MERGE_LEFT": "icons/right-arrow.png",
    "UNDO": "icons/undo-arrow.png",
    "REDO": "icons/redo-arrow.png",
    "ADD_FILE": "icons/add.png",
}


"""
Colors to be used for all styling the GUI. 
Each dictionary object should be an instance of the QColor class
"""
COLORS = {
    "LINE_DIFF": QtGui.QColor(255, 150, 150),
    "LINE_MERGE": QtGui.QColor(219, 235, 255),
    "PAD_SPACE": QtGui.QColor(240, 240, 240),
    "DEFAULT": QtGui.QColor(255, 255, 255),
    "TBL_HEADER_DEFAULT_BACKGROUND": QtGui.QColor(179, 179, 179),
    "TBL_HEADER_DEFAULT_FOREGROUND": QtGui.QColor(0, 0, 0)

}

"""
Fonts to be used throughout the GUI
"""
FONTS = {
    "TBL_HEADER_DEFAULT": QtGui.QFont('Open Sans Bold', weight=QtGui.QFont.Bold, pointSize=12),
    "TOOLBAR_DEFAULT": QtGui.QFont('Open Sans Bold', weight=QtGui.QFont.Bold)
}