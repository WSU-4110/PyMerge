"""
###########################################################################
File:
Author:
Description:


Copyright (C) 2019

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

import changeset
import longest_common_subseq
import pymerge_enums


def get_next_idx_match(match_list: list or set, curr_idx: int) -> list:
    """
    Gets the next matching index set from a padded LCS output list
    :param match_list: padded LCS output list
    :param curr_idx: current index that the calling function is at
    :return: list containing the next index match pair
    """
    for n in range(curr_idx, len(match_list[0])):
        try:
            if match_list[0][n] != -1 and match_list[1][n] != -1:
                return [match_list[0][n], match_list[1][n]]
        except IndexError:
            return [-1, -1]


def diff_set(
    file_a,
    file_b,
    file_a_path,
    file_b_path,
    change_set_a: changeset.ChangeSet,
    change_set_b: changeset.ChangeSet,
):
    """
    This function gets the diff between two files and adds each line to a change set.
    Flags are set for each lines depending on if the lines were changes, added, or are the same.
    :param file_a: left hand file to compare
    :param file_b: right hand file to compare
    :param change_set_a: change set object for the left file
    :param change_set_b: change set object for the right file
    :return: pmEnums.CHANGED value indicating if operation was successful
    """

    file_a_lines: list = file_a.read().splitlines()
    file_b_lines: list = file_b.read().splitlines()
    last_vals: list = [0, 0]  # Last found match indices

    # Get the raw, padded LCS output
    file_a_lines.append(
        "$"
    )  # Append a token on the end to make sure last 'lines' always match
    file_b_lines.append("$")
    raw_diff: list = longest_common_subseq.padded_lcs(
        file_a_lines, file_b_lines, max(len(file_a_lines), len(file_b_lines))
    )

    for n in range(len(raw_diff[0])):
        if raw_diff[0][n] != -1 and raw_diff[1][n] != -1:
            change_set_a.add_change(
                n, pymerge_enums.CHANGEDENUM.SAME, file_a_lines[raw_diff[0][n]]
            )
            change_set_b.add_change(
                n, pymerge_enums.CHANGEDENUM.SAME, file_b_lines[raw_diff[1][n]]
            )
            last_vals = [raw_diff[0][n], raw_diff[1][n]]

        else:
            # If the delta between the next match indices and the previous match indices is equal, just set to diff
            if (
                (0 < n < len(raw_diff[0]) - 1)
                and ((raw_diff[0][n - 1] + 2) == raw_diff[0][n + 1])
                or ((raw_diff[1][n - 1] + 2) == raw_diff[1][n + 1])
            ):
                change_set_a.add_change(
                    n, pymerge_enums.CHANGEDENUM.CHANGED, file_a_lines[raw_diff[0][n - 1] + 1]
                )
                change_set_b.add_change(
                    n, pymerge_enums.CHANGEDENUM.CHANGED, file_b_lines[raw_diff[1][n - 1] + 1]
                )
            else:
                # Get the next matching indices
                next_vals = get_next_idx_match(raw_diff, n)

                if next_vals == [-1, -1]:
                    return pymerge_enums.RESULT.ERROR

                idx_delta = [next_vals[0] - last_vals[0], next_vals[1] - last_vals[1]]

                # If the match index deltas are equal the line flags can default to CHANGED
                if idx_delta[0] == idx_delta[1]:
                    last_vals = [x + 1 for x in last_vals]
                    change_set_a.add_change(
                        n, pymerge_enums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]]
                    )
                    change_set_b.add_change(
                        n, pymerge_enums.CHANGEDENUM.CHANGED, file_b_lines[last_vals[1]]
                    )

                # If the delta is greater on the left side, that means lines were inserted in the left file
                elif idx_delta[0] > idx_delta[1]:
                    # Check if the last index matches are getting close to to the next index matches
                    if last_vals[1] < (next_vals[1] - 1):
                        last_vals = [x + 1 for x in last_vals]
                        change_set_a.add_change(
                            n, pymerge_enums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]]
                        )
                        change_set_b.add_change(
                            n, pymerge_enums.CHANGEDENUM.CHANGED, file_b_lines[last_vals[1]]
                        )
                    else:
                        last_vals = [x + 1 for x in last_vals]
                        change_set_a.add_change(
                            n, pymerge_enums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]]
                        )
                        change_set_b.add_change(n, pymerge_enums.CHANGEDENUM.ADDED, "")

                # if the delta is greater on the right side, that means lines were inserted in the right file
                elif idx_delta[0] < idx_delta[1]:
                    if last_vals[0] < (next_vals[0] - 1):
                        last_vals = [x + 1 for x in last_vals]
                        change_set_a.add_change(
                            n, pymerge_enums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]]
                        )
                        change_set_b.add_change(
                            n, pymerge_enums.CHANGEDENUM.CHANGED, file_b_lines[last_vals[1]]
                        )

                    else:
                        last_vals = [x + 1 for x in last_vals]
                        change_set_a.add_change(n, pymerge_enums.CHANGEDENUM.ADDED, "")
                        change_set_b.add_change(
                            n, pymerge_enums.CHANGEDENUM.CHANGED, file_b_lines[last_vals[1]]
                        )

                else:
                    # The default flag is CHANGED
                    change_set_a.add_change(
                        n, pymerge_enums.CHANGEDENUM.CHANGED, file_a_lines[raw_diff[0][n]]
                    )
                    change_set_b.add_change(
                        n, pymerge_enums.CHANGEDENUM.CHANGED, file_b_lines[raw_diff[1][n]]
                    )

    return pymerge_enums.RESULT.GOOD
