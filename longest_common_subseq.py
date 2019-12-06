"""
###########################################################################
File: longest_common_subseq.py
Author:
Description: Implementation of the longest common subsequence algorithm.


Copyright (C) PyMerge Team 2019

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
###########################################################################
"""

use_cython = False

try:
    from cython_accelerator import lcs_cython
except ImportError:
    use_cython = False


USE_MYERS_DIFF = True


def mat_print(mat):
    for row in mat:
        print(row)


def longest_common_subsequence2(left_set, right_set):
    left_set_size = len(left_set)
    right_set_size = len(right_set)
    total_size = left_set_size + right_set_size
    array_size = 2 * total_size + 1
    bounded_array = [0] * array_size
    k_candidates = [None] * array_size
    outp = [[], []]

    for d in range(total_size + 1):
        for k in range(-d, d + 1, 2):
            if k == -d or (
                k != d and bounded_array[total_size + k - 1] < bounded_array[total_size + k + 1]
            ):
                idx = total_size + k + 1
                x_idx = bounded_array[idx]
            else:
                idx = total_size + k - 1
                x_idx = bounded_array[idx] + 1
            y_idx = x_idx - k
            snake = k_candidates[idx]
            while x_idx < len(left_set) and y_idx < len(right_set) and left_set[x_idx] == right_set[y_idx]:
                snake = ((x_idx, y_idx), snake)
                x_idx += 1
                y_idx += 1
            if x_idx >= len(left_set) and y_idx >= len(right_set):
                while snake:
                    outp[0].append(snake[0][0])
                    outp[1].append(snake[0][1])
                    snake = snake[1]
                outp[0].reverse()
                outp[1].reverse()
                return outp
            bounded_array[total_size + k] = x_idx
            k_candidates[total_size + k] = snake


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
    if use_cython:
        outp = lcs_cython.padded_lcs(right_set, left_set, myers=USE_MYERS_DIFF)
        return outp
    else:
        raw_matches = longest_common_subsequence2(right_set, left_set)
        return pad_raw_line_matches(raw_matches, file_length_max)
