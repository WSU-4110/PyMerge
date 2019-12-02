"""
###########################################################################
File: diff_interface.py
Author:
Description: Python interface for the longest common subsequence executable.


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