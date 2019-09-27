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
    lcs_matrix = []  # Declare the subsequence matrix
    idx_matches = [[], []]  # Index matches
    right_size = len(right_set)  # Calculate the size only once
    left_size = len(left_set)

    for i in range(right_size + 1):
        row = []
        for j in range(left_size + 1):
            row.append(0)
        lcs_matrix.append(row)

    # Convert subsequence matrix to numpy array to make larger comparisons more efficient
    lcs_matrix = np.array(lcs_matrix)

    for i in range(right_size + 1):
        for j in range(left_size + 1):
            if i == 0 or j == 0:
                lcs_matrix[i][j] = 0
            elif right_set[i - 1] == left_set[j - 1]:
                lcs_matrix[i][j] = lcs_matrix[i - 1][j - 1] + 1
            else:
                lcs_matrix[i][j] = max(lcs_matrix[i - 1][j], lcs_matrix[i][j - 1])

    idx = lcs_matrix[right_size][left_size]

    lcs = ["" for x in range(idx + 1)]

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
            idx_matches[0].append(None)
            idx_matches[1].append(None)
        else:
            j = j - 1
            idx_matches[0].append(None)
            idx_matches[1].append(None)

    idx_matches[0].reverse()
    idx_matches[1].reverse()

    return idx_matches