from longest_common_subseq import longest_common_subsequence
from difflib import SequenceMatcher



def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



file1 = open("test_file1.txt","r").read()
file2 = open("test_file2.txt","r").read()

file1_line_array = open("test_file1.txt","r").readlines()
file2_line_array = open("test_file2.txt","r").readlines()


for line in range(len(file1_line_array)):
	file1_line_array[line] = file1_line_array[line].strip('\n')

for line in range(len(file2_line_array)):
	file2_line_array[line] = file2_line_array[line].strip('\n')



diff = longest_common_subsequence(file1, file2)

file1_diff = diff[0]
file2_diff = diff[1]



# print("")
# for i in range(len(file1_diff)):
# 	print('{:10s} {:20s}'.format(str(file1_diff[i]), str(file2_diff[i])))
# print("\n")




f1_lines_inclusive = []
f2_lines_inclusive = []

line = ""

for i in file1_diff:
	if file1[i] == "\n":
		f1_lines_inclusive.append(line)
		line = ""
	else:
		line = line + file1[i]
f1_lines_inclusive.append(line)

line = ""

for i in file2_diff:
	if file2[i] == "\n":
		f2_lines_inclusive.append(line)
		line = ""
	else:
		line = line + file2[i]
f2_lines_inclusive.append(line)



f1_same_lines = []

for line in range(len(file1_line_array)):
	f1_same_lines.append(similar(file1_line_array[line], f1_lines_inclusive[line]))


fileA = open("test_file1.txt","r")
fileB = open("test_file2.txt","r").readlines()



lines = []
string = ""

for i in fileA.read():
	if i == '\n':
		lines.append(string)
		string = ""
	else:
		string = string + i
lines.append(string)

print(lines)

# print(fileA.readlines())


print("\n")




	