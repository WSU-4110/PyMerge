import numpy as np


def mat_print(mat):
    for row in mat:
        print(row)


"""
This needs a lot of optimization because the runtime grows quadratically, as does the space.
For two files that each have 1000 lines with an average of 10 words per line the following would occur:
    - 1000000 comparisons
    - tested with 32000 lines on my laptop used like 8GB of memory

"""


def longest_common_subsequence(right_set, left_set):
    idx_matches = [[], []]  # Index matches
    right_size = len(right_set)  # Calculate the size only once
    left_size = len(left_set)
    lcs_matrix = [[0 for x in range(left_size + 1)] for y in range(right_size + 1)]  # Declare the sub-sequence matrix

    # Convert subsequence matrix to numpy array to make larger comparisons more efficient
    lcs_matrix = np.array(lcs_matrix)

    for i in range(right_size + 1):
        for j in range(left_size + 1):
            if i == 0 or j == 0:
                lcs_matrix[i][j] = 0
            if right_set[i - 1] == left_set[j - 1]:
                lcs_matrix[i][j] = lcs_matrix[i - 1][j - 1] + 1
            else:
                lcs_matrix[i][j] = max(lcs_matrix[i - 1][j], lcs_matrix[i][j - 1])

    idx = lcs_matrix[right_size][left_size]

    lcs = [""] * (idx + 1)

    i = right_size
    j = left_size
    while i > 0 and j > 0:
        if right_set[i - 1] == left_set[j - 1]:
            lcs[idx - 1] = right_set[i - 1]
            idx_matches[0].append(i - 1)
            idx_matches[1].append(j - 1)
            i = i - 1
            j = j - 1
            idx = idx - 1

        elif lcs_matrix[i - 1][j] > lcs_matrix[i][j - 1]:
            i = i - 1
        else:
            j = j - 1

    idx_matches[0].reverse()
    idx_matches[1].reverse()

    return idx_matches


# Pass your match list to this
def pad_raw_line_matches(match_list):
    m = len(match_list[0])
    n = len(match_list[1])
    idx = 1
    cntr = 0
    outp_list = [[], []]

    print("Table #      Right #     Left #")
    while cntr < min(m, n):
        for r in range(
                max(match_list[0][idx] - match_list[0][idx - 1], match_list[1][idx] - match_list[1][idx - 1]) - 1):
            outp_list[0].append(None)
            outp_list[1].append(None)
            # print(cntr + 1, "\t\t\t", "")
            cntr += 1
        # print(cntr + 1, "\t\t\t", match_list[0][idx] + 1, "\t\t\t", match_list[1][idx] + 1)
        outp_list[0].append(match_list[0][idx] + 1)
        outp_list[1].append(match_list[1][idx] + 1)
        idx += 1
        cntr += 1

    return outp_list