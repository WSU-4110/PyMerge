# from changeSet import change_set
import changeSet
import longest_common_subseq
import pmEnums
import time

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
    iFileA, iFileB, file_a_path, file_b_path, ochangeSetA: changeSet.ChangeSet, ochangeSetB: changeSet.ChangeSet
):
    """
    This function gets the diff between two files and adds each line to a change set.
    Flags are set for each lines depending on if the lines were changes, added, or are the same.
    :param iFileA: left hand file to compare
    :param iFileB: right hand file to compare
    :param ochangeSetA: change set object for the left file
    :param ochangeSetB: change set object for the right file
    :return: pmEnums.CHANGED value indicating if operation was successful
    """

    file_a_lines: list = iFileA.read().splitlines()
    file_b_lines: list = iFileB.read().splitlines()
    last_vals: list = [0, 0]  # Last found match indices
    next_vals: list = [0, 0]  # Next match indices

    # Get the raw, padded LCS output
    file_a_lines.append(
        "$"
    )  # Append a token on the end to make sure last 'lines' always match
    file_b_lines.append("$")
    raw_diff: list = longest_common_subseq.padded_lcs(
        file_a_lines, file_b_lines, max(len(file_a_lines), len(file_b_lines))
    )

    start = time.time()
    #raw_diff = longest_common_subseq.lcs_c_if(file_a_path, file_b_path, "test.xml")
    #print(raw_diff)
    end = time.time()
    print(end - start)
    #print(raw_diff)
    for n in range(len(raw_diff[0])):
        if raw_diff[0][n] != -1 and raw_diff[1][n] != -1:
            ochangeSetA.add_change(
                n, pmEnums.CHANGEDENUM.SAME, file_a_lines[raw_diff[0][n]]
            )
            ochangeSetB.add_change(
                n, pmEnums.CHANGEDENUM.SAME, file_b_lines[raw_diff[1][n]]
            )
            last_vals = [raw_diff[0][n], raw_diff[1][n]]

        else:
            # If the delta between the next match indices and the previous match indices is equal, just set to diff
            if (
                (0 < n < len(raw_diff[0]) - 1)
                and ((raw_diff[0][n - 1] + 2) == raw_diff[0][n + 1])
                or ((raw_diff[1][n - 1] + 2) == raw_diff[1][n + 1])
            ):
                ochangeSetA.add_change(
                    n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[raw_diff[0][n - 1] + 1]
                )
                ochangeSetB.add_change(
                    n, pmEnums.CHANGEDENUM.CHANGED, file_b_lines[raw_diff[1][n - 1] + 1]
                )
            else:
                # Get the next matching indices
                next_vals = get_next_idx_match(raw_diff, n)

                if next_vals == [-1, -1]:
                    return pmEnums.RESULT.ERROR

                idx_delta = [next_vals[0] - last_vals[0], next_vals[1] - last_vals[1]]

                # If the match index deltas are equal the line flags can default to CHANGED
                if idx_delta[0] == idx_delta[1]:
                    last_vals = [x + 1 for x in last_vals]
                    ochangeSetA.add_change(
                        n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]]
                    )
                    ochangeSetB.add_change(
                        n, pmEnums.CHANGEDENUM.CHANGED, file_b_lines[last_vals[1]]
                    )

                # If the delta is greater on the left side, that means lines were inserted in the left file
                elif idx_delta[0] > idx_delta[1]:
                    # Check if the last index matches are getting close to to the next index matches
                    if last_vals[1] < (next_vals[1] - 1):
                        last_vals = [x + 1 for x in last_vals]
                        ochangeSetA.add_change(
                            n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]]
                        )
                        ochangeSetB.add_change(
                            n, pmEnums.CHANGEDENUM.CHANGED, file_b_lines[last_vals[1]]
                        )
                    else:
                        last_vals = [x + 1 for x in last_vals]
                        ochangeSetA.add_change(
                            n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]]
                        )
                        ochangeSetB.add_change(n, pmEnums.CHANGEDENUM.ADDED, "")

                # if the delta is greater on the right side, that means lines were inserted in the right file
                elif idx_delta[0] < idx_delta[1]:
                    if last_vals[0] < (next_vals[0] - 1):
                        last_vals = [x + 1 for x in last_vals]
                        ochangeSetA.add_change(
                            n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]]
                        )
                        ochangeSetB.add_change(
                            n, pmEnums.CHANGEDENUM.CHANGED, file_b_lines[last_vals[1]]
                        )

                    else:
                        last_vals = [x + 1 for x in last_vals]
                        ochangeSetA.add_change(n, pmEnums.CHANGEDENUM.ADDED, "")
                        ochangeSetB.add_change(
                            n, pmEnums.CHANGEDENUM.CHANGED, file_b_lines[last_vals[1]]
                        )

                else:
                    # The default flag is CHANGED
                    ochangeSetA.add_change(
                        n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[raw_diff[0][n]]
                    )
                    ochangeSetB.add_change(
                        n, pmEnums.CHANGEDENUM.CHANGED, file_b_lines[raw_diff[1][n]]
                    )

    return pmEnums.RESULT.GOOD
