"""
various enumerations, to standardize the output and input that functions 
are expecting to get. 
"""
from enum import Enum

class RESULT( Enum ):
    GOOD = 0
    ERROR = 1
    NOTIMPL = 2 #not implemented
    FILEMISMAT = 3 #file mismatch

class ATTRIB( Enum ):
    DATA = 0
    CHANGE = 1

class CHANGEDENUM( Enum ):
    SAME = 0
    CHANGED = 1
    ADDED = 2
    MOVED = 3
    PADDING = 4
    ERROR = 5

    
