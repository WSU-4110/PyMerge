
# Cases:
# 	- changed letter in word 
# 	- changed word in line 
# 	- multiple changed words in line 
# 	- replaced line --> check how similar the 2 lines are 
# 	- deleted line 
# 	- added line

# create another class that stores change information about a particular line 
# number of lines in file == number of change objects 


import filecmp 


class Changes:
	def __init__(self)

	

class PyMerge:

	def __init__(self, file):
		self.fileName = file
		# change to 2D array that stores changed line in row and changed index/indies
		self.diffLinesList = []	

	def printFile(self):
		file = open(self.fileName, "r")
		for line in self.file:
			print(line)

	def check_if_same(self, fileName2):
		return filecmp.cmp(self.fileName, fileName2)

	def get_inconsistent_lines(self, fileName2):
		lineNum = 1
		with open(self.fileName) as file1:
			with open(fileName2) as file2:
				for line1,line2 in zip(file1, file2):
					if line1 != line2:
						self.diffLinesList.append(lineNum)
					lineNum += 1
		return self.diffLinesList

	# def show_changes(self, fileName2, lineNum):
	# 	with open(self.fileName) as file1:
	# 		with open(fileName2) as file2:
	# 			for line in file1:
	# 				print(line)
				


def count_lines(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

f1 = "test_file_1.txt"
f2 = "test_file_2.txt"

file1 = open(f1, "r")
file2 = open(f2, "r")

f1_lines = file1.readlines()
f2_lines = file2.readlines()

if len(f1_lines) > len(f2_lines):
	number_of_lines = len(f1_lines)
else:
	number_of_lines = len(f2_lines)


changed_lines = []

for line in range(number_of_lines):

	if len(f1_lines[line]) < len(f2_lines[line]):
		line_len = len(f1_lines[line])
	else:
		line_len = len(f2_lines[line])

	changes_in_line = []

	for char in range(line_len):

		if f1_lines[line][char] != f2_lines[line][char]:
			if line not in changed_lines:
				changed_lines.append(line)
			changes_in_line.append(char)



