"""
algorithm class. Must be provided with two files, and two changeSet objects. It will compare
the files and populate the ChangeSet Objects
"""
import pmEnums
import changeSet

class algorithm:
    def __init__(self):
        pass
    
    def generateChangeSets( self, iFileA, iFileB, ochangeSetA, ochangeSetB ):
        # file line 1 = stringA
        # ioFileA.attributeStorageVariable = stringA
        
        f1 = iFileA.readlines()
        f2 = iFileB.readlines()

        # return pmEnums.RESULT.NOTIMPL


file1 = open("test_file1.txt", "r")
file2 = open("test_file2.txt", "r")

file1Changes = ChangeSet()
file2Changes = ChangeSet()

alg = algorithm()
alg.generateChangeSets(file1, file2, file1Changes, file2Changes)



    
