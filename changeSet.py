"""
changeSet class, provides a data structure to make working with file differences (change sets)
easier by abstracting the data storage, and providing a single accessor function.
"""
import pmEnums
    
class changeSet:

    def __init__():
        pass
        
    def access( ilineNum, iattrib, oreturnObj ):
        oreturnObj[0] = pmEnums.CHANGEDENUM.CHANGED
        return pmEnums.RESULT.NOTIMPL

    #some private list to store all the strings at easy line numbers
    #__dataListA = []
    #__dataListB = []
