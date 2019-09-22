"""
This is the entry point for the PyMerge program. Command line arguments will be passed
to this file and the functions in this file will invoke the GUI. There will be no merge/compare/GUI
algorithms in this file. It will only call the main GUI and application functions.

"""

import sys
import os


class CLI(object):
    def __init__(self, *args):
        for arg in args:
            print(arg)



if __name__ == '__main__':
    CLI(sys.argv)