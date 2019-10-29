#cython: boundscheck=False
#standard cimport file libc/stdlib.pxd
#cython: language_level=3
#cythonL optimize.use_switch=True
#cython: infer_types=True
#cython: initializedcheck=False
#cython: optimize.unpack_method_calls=True
#cython: cdivision=True
#cython: Cython.Compiler.Options.gcc_branch_hints=True
#cython: Cython.Compiler.Options.lookup_module_cpdef=False
#cython: Cython.Compiler.Options.cache_builtins=True
#cython: Cython.Compiler.Options.clear_to_none=False
#cython: Cython.wraparound=False

malloc, free


cdef longest_common_subsequence(right_set, left_set):
    idx_matches = [[], []]  # Index matches
    cdef unsigned int right_size = len(right_set)  # Calculate the size only once
    cdef unsigned int left_size = len(left_set)
    lcs_matrix = [[0 for x in range(left_size + 1)] for y in range(right_size + 1)]  # Declare the sub-sequence matrix
    cdef unsigned int i_ = 0
    cdef unsigned int j_ = 0

    for i in range(right_size + 1):
        for j in range(left_size + 1):
            if i == 0 or j == 0:
                lcs_matrix[i][j] = 0
            if right_set[i - 1] == left_set[j - 1]:
                lcs_matrix[i][j] = lcs_matrix[i - 1][j - 1] + 1
            else:
                lcs_matrix[i][j] = max(lcs_matrix[i - 1][j], lcs_matrix[i][j - 1])

    cdef unsigned int idx = lcs_matrix[right_size][left_size]

    lcs = [""] * (idx + 1)

    i_ = right_size
    j_ = left_size
    while i_ > 0 and j_ > 0:
        if right_set[i_ - 1] == left_set[j_ - 1]:
            lcs[idx - 1] = right_set[i_ - 1]
            idx_matches[0].append(i_ - 1)
            idx_matches[1].append(j_ - 1)
            i_ -= 1
            j_ -= 1
            idx -= 1

        elif lcs_matrix[i_ - 1][j_] > lcs_matrix[i_][j_ - 1]:
            i_ -= 1
        else:
            j_ -= 1

    idx_matches[0].reverse()
    idx_matches[1].reverse()

    return idx_matches


# Pass your match list to this
cdef pad_raw_line_matches(match_list, int file_length_max):
    cdef unsigned int m = len(match_list[0])
    cdef unsigned int n = len(match_list[1])
    cdef int idx = 0
    cdef int cntr = 0
    outp_list = [[], []]
    cdef unsigned int r_ = 0
    cdef unsigned int n_ = 0

    while r_ < (
            max(match_list[0][idx] - 0, match_list[1][idx] - 0) - 1):
        outp_list[0].append(-1)
        outp_list[1].append(-1)
        r_ += 1
    r_ = 0

    while n_ < max(m, n):
        while r_ < (
                max(match_list[0][idx] - match_list[0][idx - 1], match_list[1][idx] - match_list[1][idx - 1]) - 1):
            outp_list[0].append(-1)
            outp_list[1].append(-1)
            cntr += 1
            r_ += 1
        outp_list[0].append(match_list[0][idx])
        outp_list[1].append(match_list[1][idx])
        idx += 1
        cntr += 1
        n_ += 1

    return outp_list


def padded_lcs(right_set, left_set):
    raw_matches = longest_common_subsequence(right_set, left_set)
    return pad_raw_line_matches(raw_matches, 0)
