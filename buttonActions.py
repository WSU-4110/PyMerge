"""
Buttons pressed will call these functions, 
these functions will make the appropriate function calls.
"""

import pmEnums

class buttonActions:
    def mergeLeft():
        print("mergeL")
        return pmEnums.RESULT.NOTIMPL

    def mergeRight():
        print("mergeR")
        return pmEnums.RESULT.NOTIMPL
    
    def openFile():
        print("open file")
        return pmEnums.RESULT.NOTIMPL
    
    def previousDiff():
        print("prev diff")
        return pmEnums.RESULT.NOTIMPL
    
    def nextDiff():
        print("next diff")
        return pmEnums.RESULT.NOTIMPL

    def undoChange():
        print("undo")
        return pmEnums.RESULT.NOTIMPL

    def redoChange():
        print("redo")
        return pmEnums.RESULT.NOTIMPL
