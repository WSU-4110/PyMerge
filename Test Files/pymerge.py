import filecmp 

class PyMerge:

	def __init__(self, file):
		self.fileName = file	

	def printFile(self):
		file = open(self.fileName, "r")
		for line in self.file:
			print(line)

	def checkIfSame(self, fileName2):
		return filecmp.cmp(self.fileName, fileName2)

	def diffLines(self, fileName2):
		lineNum = 1
		lineArray = []
		with open(self.fileName) as file1:
			with open(fileName2) as file2:
				for line1,line2 in zip(file1, file2):
					if line1 != line2:
						lineArray.append(lineNum)
					lineNum += 1
		return lineArray

	def showChanges(self, fileName2, lineNum):
		with open(self.fileName) as file1:
			with open(fileName2) as file2:
				


if __name__ == "__main__":

	file1 = "test_file_1.txt"
	file2 = "test_file_2.txt"
	file = PyMerge(file1)
	changedLineArray = file.diffLines(file2)
	file.showChanges(file2, changedLineArray[0])
       
    

		

