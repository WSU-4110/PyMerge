import subprocess
from xml.etree import ElementTree as ET

import longest_common_subseq


def lcs_c_if(left_file, right_file, outp_file):
    ret_obj = subprocess.run(["LCS_C/build/LCS", right_file, left_file, outp_file], stdout=subprocess.PIPE)
    raw_matches = [[], []]

    tree = ET.parse(outp_file)
    root = tree.getroot()

    for row in root.iter("match"):
        try:
            raw_matches[0].append(int(row.attrib["left"]))
            raw_matches[1].append(int(row.attrib["right"]))
        except (TypeError, ValueError) as err:
            print("Type error in diff interface!")
            raw_matches.append([-1, -1])

    raw_matches[0] = raw_matches[0][:-1]
    raw_matches[1] = raw_matches[1][:-1]
    outp = longest_common_subseq.pad_raw_line_matches(raw_matches, -1)

    return outp