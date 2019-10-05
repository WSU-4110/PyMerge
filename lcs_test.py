from longest_common_subseq import longest_common_subsequence

file1 = open("test_file1.txt","r").read()
file2 = open("test_file2.txt","r").read()

diff = longest_common_subsequence(file1, file2)

file1_diff = diff[0]
file2_diff = diff[1]

# print(file1_diff)

sim_list = []

for index in file1_diff:
	if index != None:
		if file1[index] == "\n":
			file1_diff[index] = "EndLine"

print(file1_diff)
