"""
fileIO class, providing an interface for the GUI to input files, and get changeSets. After the GUI has two
changeSet objects, it is able to handle the rest of the application requirements on its
own untill it is time to write changes. 
"""
import pmEnums
import changeSet
import algorithm

class fileIO:    
    @staticmethod
    def diffFiles( iFileA, iFileB ):
        changesA = changeSet.changeSet
        changesB = changeSet.changeSet
        
        fileA = open(iFileA, 'r')
        fileB = open(iFileB, 'r')

        alg = algorithm.algorithm
        result = alg.generateChangeSets(fileA, fileB, changesA, changesB)

        fileA.close()
        fileB.close()
        
        if result == pmEnums.RESULT.GOOD:        
            return pmEnums.RESULT.GOOD
        return pmEnums.RESULT.NOTIMPL

    @staticmethod
    def getChangeSets( oFileA, oFileB):
        oFileA = changesA
        oFileB = changesB 
        if changesA != 0 or changesB != 0:
            return changeSet.GOOD
        return changeSet.ERROR
    
