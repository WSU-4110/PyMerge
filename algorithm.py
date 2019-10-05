"""
algorithm class. Must be provided with two files, and two changeSet objects. It will compare
the files and populate the ChangeSet Objects
"""
from longest_common_subseq import longest_common_subsequence
from difflib import SequenceMatcher
import pmEnums
import changeSet
import os



class algorithm:
    def __init__(self):
        pass

    def similar(self, fileA, fileB):
        return SequenceMatcher(None, fileA, fileB).ratio()

    def strip_end_lines(self, file_line_array):
        for line in range(len(file_line_array)):
            file_line_array[line] = file_line_array[line].strip('\n')
        return file_line_array

    def generateInclusiveList(self, origFile, diffFile):

        inclusiveLines = []

        line = ""

        for i in diffFile:
            if origFile[i] == "\n":
                inclusiveLines.append(line)
                line = ""
            else:
                line = line + origFile[i]
        inclusiveLines.append(line)

        return inclusiveLines

    def readLines(self, file):

        string = ""
        file_line_array = []

        for i in file:
            if i == '\n':
                file_line_array.append(string)
                string = ""
            else:
                string = string + i
        file_line_array.append(string)

        return file_line_array

    
    def generateChangeSets( self, iFileA, iFileB, ochangeSetA, ochangeSetB ):
        #NO DONT REMOVE THIS RETURN STATEMENT
        #UNTILL THE FUNCTION IS FINISHED BEING IMPLEMENTED

        fileA = iFileA.read()
        fileB = iFileB.read()

        fileA_line_array = self.readLines(fileA)
        fileB_line_array = self.readLines(fileA)
        
        self.strip_end_lines(fileA_line_array)
        self.strip_end_lines(fileB_line_array)

        diff = longest_common_subsequence(fileA, fileB)

        fileA_diff = diff[0]
        fileB_diff = diff[1]

        fileA_inclusive_lines = self.generateInclusiveList(fileA, fileA_diff)
        fileB_inclusive_lines = self.generateInclusiveList(fileB, fileB_diff)

        fileA_same_lines = []
        fileB_same_lines = []

        for line in range(len(fileA_line_array)):
            fileA_same_lines.append(self.similar(fileA_line_array[line], fileA_inclusive_lines[line]))

        for line in range(len(fileB_line_array)):
            fileB_same_lines.append(self.similar(fileB_line_array[line], fileB_inclusive_lines[line]))

        print(fileA_same_lines)

        return pmEnums.RESULT.NOTIMPL

        # return pmEnums.RESULT.ERROR
        # return pmEnums.RESULT.GOOD


file1Changes = changeSet.ChangeSet()
file2Changes = changeSet.ChangeSet()

#alg = algorithm()
#alg.getChangeSets("test_file1.txt", "test_file2.txt", file1Changes, file2Changes)


file1 = open("test_file1.txt","r")
file2 = open("test_file2.txt","r")

diff = algorithm()
diff.generateChangeSets(file1, file2, file1Changes, file2Changes)



    
