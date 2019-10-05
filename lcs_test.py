from longest_common_subseq import longest_common_subsequence

file1 = open("test_file1.txt","r").read()
file2 = open("test_file2.txt","r").read()

# f1_lines = open("test_file1.txt","r").readlines()
# f2_lines = open("test_file2.txt","r").readlines()

diff = longest_common_subsequence(file1, file2)

file1_diff = diff[0]
file2_diff = diff[1]


# for i in range(len(file1)):
# 	if file1[i] == "\n":
# 		file1_diff[i] = "EndLine"

# for i in range(len(file2)):
# 	if file2[i] == "\n":
# 		file2_diff[i] = "EndLine"


print("")
for i in range(len(file1_diff)):
	print('{:10s} {:20s}'.format(str(file1_diff[i]), str(file2_diff[i])))
print("\n\n")


f1_lines_inclusive = []
f2_lines_inclusive = []

begLine = 0
endLine = 0

i_file1_diff = -1

for i in range(len(file1)):
	i_file1_diff += 1
	while (file1_diff[i_file1_diff] == None):
		i_file1_diff += 1
	print(i_file1_diff)


print("\n")
	