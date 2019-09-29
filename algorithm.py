"""
algorithm class. Must be provided with two files, and two changeSet objects. It will compare
the files and populate the ChangeSet Objects
"""
from pmEnums import CHANGEDENUM
import changeSet

class algorithm:
    def __init__(self):
        pass
    
    def getChangeSets( self, iFileA, iFileB, ochangeSetA, ochangeSetB ):
        # file line 1 = stringA
        # ioFileA.attributeStorageVariable = stringA
        
        f1 = iFileA.readlines()
        f2 = iFileB.readlines()

        for line in range(len(f1)):
        	if f1[line] == f2[line]:
        		file1Changes.setChange(line, CHANGEDENUM.SAME, f1[line])
        	else:
        		file1Changes.setChange(line, CHANGEDENUM.CHANGED, f1[line])

        return RESULT.NOTIMPL


file1 = open("test_file1.txt", "r")
file2 = open("test_file2.txt", "r")

file1Changes = changeSet.ChangeSet()
file2Changes = changeSet.ChangeSet()

alg = algorithm()
alg.getChangeSets(file1, file2, file1Changes, file2Changes)






    
