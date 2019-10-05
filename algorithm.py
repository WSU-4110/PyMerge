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
    
    def generateChangeSets( self, iFileNameA, iFileNameB, ochangeSetA, ochangeSetB ):
        #NO DONT REMOVE THIS RETURN STATEMENT
        #UNTILL THE FUNCTION IS FINISHED BEING IMPLEMENTED
        return pmEnums.RESULT.NOTIMPL
        # file line 1 = stringA
        # ioFileA.attributeStorageVariable = stringA
        
        f1 = open(iFileNameA).readlines()
        f2 = open(iFileNameB).readlines()

        f1_name, f1_ext = os.path.splitext(iFileNameA)
        f2_name, f2_ext = os.path.splitext(iFileNameB)

        # if inconsistent file types 
        if f1_ext != f2_ext:
            print("[-] Incompatible file types", f1_ext, "and", f2_ext)
            return pmEnums.RESULT.FILEMISMAT

        # stack to store lines that did not match up --> used for later comparison to determine
        # if line was moved or added 
        stack = []

        for line in range(len(f1)):

            # if both lines are the same 
            if f1[line] == f2[line]:
                file1Changes.addChange(line+1, pmEnums.CHANGEDENUM.SAME, f1[line])

            else:
                temp_list = [line+1, -1, f1[line]]
                stack.append(temp_list)

                # *********** find way to determine if line was changed ***********
                # file1Changes.addChange(line+1, pmEnums.CHANGEDENUM.CHANGED, f1[line])

            # if line in stack (from f1) matches up with current line being compared in f2, 
            # then the line in f1 was moved 
            for stack_item in stack:
                if stack_item[2] == f2[line]:
                    stack_item[1] = pmEnums.CHANGEDENUM.MOVED
                    item = stack.pop(stack.index(stack_item))
                    file1Changes.addChange(item[0], item[1], item[2])

        # items that remain in stack were never found in f2 and therefore were added 
        for stack_item in stack:
            stack_item[1] = pmEnums.CHANGEDENUM.ADDED
            item = stack.pop(stack.index(stack_item))
            file1Changes.addChange(item[0], item[1], item[2])
    
        return pmEnums.RESULT.NOTIMPL

        # return pmEnums.RESULT.ERROR
        # return pmEnums.RESULT.GOOD


file1Changes = changeSet.ChangeSet()
file2Changes = changeSet.ChangeSet()

#alg = algorithm()
#alg.getChangeSets("test_file1.txt", "test_file2.txt", file1Changes, file2Changes)





    
