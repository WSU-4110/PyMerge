"""
algorithm class. Must be provided with two files, and two changeSet objects. It will compare
the files and populate the ChangeSet Objects
"""
import pmEnums
import changeSet
import os

class algorithm:
    def __init__(self):
        pass
    
    def getChangeSets( self, iFileNameA, iFileNameB, ochangeSetA, ochangeSetB ):
        # file line 1 = stringA
        # ioFileA.attributeStorageVariable = stringA
        
        f1 = open(iFileNameA).readlines()
        f2 = open(iFileNameB).readlines()

        f1_name, f1_ext = os.path.splitext(iFileNameA)
        f2_name, f2_ext = os.path.splitext(iFileNameB)

        if f1_ext != f2_ext:
            print("[-] Incompatible file types", f1_ext, "and", f2_ext)
            return pmEnums.RESULT.FILEMISMAT

        for line in range(len(f1)):
        	if f1[line] == f2[line]:
        		file1Changes.addChange(line, pmEnums.CHANGEDENUM.SAME, f1[line])
        	else:
        		file1Changes.addChange(line, pmEnums.CHANGEDENUM.CHANGED, f1[line])


        return pmEnums.RESULT.NOTIMPL

        # return pmEnums.RESULT.ERROR
        # return pmEnums.RESULT.GOOD


file1Changes = changeSet.ChangeSet()
file2Changes = changeSet.ChangeSet()

alg = algorithm()
alg.getChangeSets("test_file1.txt", "test_file2.txt", file1Changes, file2Changes)






    
