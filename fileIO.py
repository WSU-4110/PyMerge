"""
fileIO class, providing an interface for the GUI to input files, and get changeSets. After the GUI has two
changeSet objects, it is able to handle the rest of the application requirements on its
own untill it is time to write changes. 
"""
import pmEnums
import changeSet

class fileIO:
    def __init__():
        pass
    
    def diffFiles( iFileA, iFileB ):
        #in here diff the files and populate two change sets
        #result = algorithmObj = algorithmClass()
        #result = algorithmObj.generateChangeSets( changesA, changesB )

        if result == pmEnums.RESULT.GOOD:        
            return pmEnums.RESULT.GOOD
        return pmEnums.RESULT.NOTIMPL

    def getChangeSets( oFileA, oFileB):
        oFileA = changesA
        oFileB = changesB 
        return pmEnums.RESULT.NOTIMPL

    #private
    __changesA = changeSet.changeSet()
    __changesB = changeSet.changeSet()


