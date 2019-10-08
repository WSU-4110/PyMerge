# from changeSet import change_set
import os
import pmEnums
import longest_common_subseq
import changeSet

# fileA = open("file1.c", 'r')
# fileB = open("file2.c", 'r')


def get_next_idx_match(match_list, curr_idx):
    for n in range(curr_idx, len(match_list[0])):
        try:
            if match_list[0][n] != -1 and match_list[1][n] != -1:
                return [match_list[0][n], match_list[1][n]]
        except IndexError:
            return [-1, -1]


def diff_set(iFileA, iFileB, ochangeSetA: changeSet.ChangeSet, ochangeSetB: changeSet.ChangeSet):
    file_a_lines = iFileA.read().splitlines()
    file_b_lines = iFileB.read().splitlines()
    last_vals = [0, 0]
    next_vals = [0, 0]
    raw_diff = longest_common_subseq.padded_lcs(file_a_lines, file_b_lines, max(len(file_a_lines), len(file_b_lines)))
    #print("Table #      Right #     Left #     FLAG")

    for n in range(len(raw_diff[0])):
        if raw_diff[0][n] != -1 and raw_diff[1][n] != -1:
            #print(f"{n}\t\t\t{raw_diff[0][n]}\t\t\t{raw_diff[1][n]}\t\t\t SAME")
            ochangeSetA.addChange(n, pmEnums.CHANGEDENUM.SAME, file_a_lines[raw_diff[0][n]])
            ochangeSetB.addChange(n, pmEnums.CHANGEDENUM.SAME, file_b_lines[raw_diff[1][n]])
            last_vals = [raw_diff[0][n], raw_diff[1][n]]

        else:
            if (0 < n < len(raw_diff[0]) - 1) and ((raw_diff[0][n - 1] + 2) == raw_diff[0][n + 1]) or ((raw_diff[1][n - 1] + 2) == raw_diff[1][n + 1]):
                #print(f"{n}\t\t\t{raw_diff[0][n-1] + 1}\t\t\t{raw_diff[1][n -1] + 1}\t\t\t*DIFF*** SINGLE")
                ochangeSetA.addChange(n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[raw_diff[0][n-1] + 1])
                ochangeSetB.addChange(n, pmEnums.CHANGEDENUM.CHANGED, file_b_lines[raw_diff[1][n-1] + 1])
            else:
                next_vals = get_next_idx_match(raw_diff, n)
                if (next_vals[0] - last_vals[0]) == (next_vals[1] - last_vals[1]):
                    last_vals[0] += 1
                    last_vals[1] += 1
                    #print(f"{n}\t\t\t{last_vals[0]}\t\t\t{last_vals[1]}\t\t\t*DIFF***")
                    ochangeSetA.addChange(n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]])
                    ochangeSetB.addChange(n, pmEnums.CHANGEDENUM.CHANGED, file_b_lines[last_vals[1]])

                elif (next_vals[0] - last_vals[0]) > (next_vals[1] - last_vals[1]):
                    if last_vals[1] < (next_vals[1] - 1):
                        last_vals[0] += 1
                        last_vals[1] += 1
                        #print(f"{n}\t\t\t{last_vals[0]}\t\t\t{last_vals[1]}\t\t\t*DIFF**1")
                        ochangeSetA.addChange(n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]])
                        ochangeSetB.addChange(n, pmEnums.CHANGEDENUM.CHANGED, file_b_lines[last_vals[1]])
                    else:
                        last_vals[0] += 1
                        last_vals[1] += 1
                        #print(f"{n}\t\t\t{last_vals[0]}\t\t\t-1\t\t\t*DIFF**2")
                        ochangeSetA.addChange(n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]])
                        ochangeSetB.addChange(n, pmEnums.CHANGEDENUM.ADDED, "")

                elif (next_vals[0] - last_vals[0]) < (next_vals[1] - last_vals[1]):
                    if last_vals[0] < (next_vals[0] - 1):
                        last_vals[0] += 1
                        last_vals[1] += 1
                        #print(f"{n}\t\t\t{last_vals[0]}\t\t\t{last_vals[1]}\t\t\t*DIFF**3")
                        ochangeSetA.addChange(n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[last_vals[0]])
                        ochangeSetB.addChange(n, pmEnums.CHANGEDENUM.CHANGED, file_b_lines[last_vals[1]])

                    else:
                        #print(f"{n}\t\t\t-1\t\t\t{last_vals[1] + 1}\t\t\t*DIFF**4")
                        ochangeSetA.addChange(n, pmEnums.CHANGEDENUM.SAME, "")
                        ochangeSetB.addChange(n, pmEnums.CHANGEDENUM.SAME, file_b_lines[last_vals[1]])
                        last_vals[0] += 1
                        last_vals[1] += 1
                else:
                    #print(f"{n}\t\t\t{raw_diff[0][n]}\t\t\t{raw_diff[1][n]}\t\t\t*DIFF***")
                    ochangeSetA.addChange(n, pmEnums.CHANGEDENUM.CHANGED, file_a_lines[raw_diff[0][n]])
                    ochangeSetB.addChange(n, pmEnums.CHANGEDENUM.CHANGED, file_b_lines[raw_diff[1][n]])

    return pmEnums.RESULT.GOOD

