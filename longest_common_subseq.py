import time

from cython_accelerator import lcs_cython

USE_CYTHON = False


def mat_print(mat):
    for row in mat:
        print(row)


def longest_common_subsequence(right_set, left_set):
    idx_matches = [[], []]  # Index matches
    right_size = len(right_set)  # Calculate the size only once
    left_size = len(left_set)
    lcs_matrix = [[0 for x in range(left_size + 1)] for y in range(right_size + 1)]  # Declare the sub-sequence matrix

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
def pad_raw_line_matches(match_list, file_length_max):
    m = len(match_list[0])
    n = len(match_list[1])
    idx = 0
    cntr = 0
    outp_list = [[], []]

    for r in range(
            max(match_list[0][idx] - 0, match_list[1][idx] - 0) - 1):
        outp_list[0].append(-1)
        outp_list[1].append(-1)

    for n in range(max(m, n)):
        for r in range(
                max(match_list[0][idx] - match_list[0][idx - 1], match_list[1][idx] - match_list[1][idx - 1]) - 1):
            outp_list[0].append(-1)
            outp_list[1].append(-1)
            cntr += 1
        outp_list[0].append(match_list[0][idx])
        outp_list[1].append(match_list[1][idx])
        idx += 1
        cntr += 1

    return outp_list


def padded_lcs(right_set, left_set, file_length_max):
    if USE_CYTHON:
        start = time.time()
        outp = lcs_cython.padded_lcs(right_set, left_set)
        end = time.time()
        print(end - start)
        return outp
    else:
        start = time.time()
        raw_matches = longest_common_subsequence(right_set, left_set)
        end = time.time()
        print(end - start)
        return pad_raw_line_matches(raw_matches, file_length_max)