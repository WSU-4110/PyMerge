"""
fileIO class, providing an interface for the GUI to input files, and get changeSets. After the GUI has two
changeSet objects, it is able to handle the rest of the application requirements on its
own untill it is time to write changes. 
"""
import pmEnums
import changeSet
import algorithm
import diff_resolution
import os.path
import utilities


class fileIO:
    def __init__(self):
        self.changesB = changeSet.ChangeSet()
        self.changesA = changeSet.ChangeSet()
    
    def diffFiles(self, iFileA, iFileB ):

        if utilities.bad_file_check(iFileA):
            print(iFileA, ": Unacceptable file type")
            return pmEnums.RESULT.BADFILE

        if utilities.bad_file_check(iFileB):
            print(iFileB, ": Unacceptable file type")
            return pmEnums.RESULT.BADFILE

        fileA = open(iFileA, 'r')
        fileB = open(iFileB, 'r')

        #alg = algorithm.algorithm
        #result = alg.generateChangeSets(alg, fileA, fileB, self.changesA, self.changesB)
        result = diff_resolution.diff_set(fileA, fileB, self.changesA, self.changesB)

        fileA.close()
        fileB.close()
        
        if result == pmEnums.RESULT.GOOD:        
            return pmEnums.RESULT.GOOD
        return pmEnums.RESULT.NOTIMPL

    def getChangeSets(self, oFileA, oFileB):
        oFileA = self.changesA
        oFileB = self.changesB
        if self.changesA != 0 and self.changesB != 0:
            return pmEnums.RESULT.GOOD
        return pmEnums.RESULT.ERROR
    
