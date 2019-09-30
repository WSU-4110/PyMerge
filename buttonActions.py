"""
Buttons pressed will call these functions, 
these functions will make the appropriate function calls.
"""

import pmEnums

class buttonActions:
    def mergeLeft():
        return pmEnums.RESULT.NOTIMPL

    def mergeRight():
        return pmEnums.RESULT.NOTIMPL
    
    def openFile():
        print("open file")
        return pmEnums.RESULT.NOTIMPL
    
    def previousDiff():
        return pmEnums.RESULT.NOTIMPL
    
    def nextDiff():
        return pmEnums.RESULT.NOTIMPL
