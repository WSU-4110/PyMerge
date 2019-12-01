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

"""
This is the entry point for the PyMerge program. Command line arguments will be passed
to this file and the functions in this file will invoke the GUI. There will be no merge/compare/GUI
algorithms in this file. It will only call the main GUI and application functions.

"""

import sys
import dependency_chk

dependency_chk.check()

import MainWindow
import utilities


class PyMergeCLI(object):
    def __init__(self, *args):
        self.options: list = self.sanitize(args[0][1:])
        self.file_size_lim: int = 2000000        
        self.cli()

    def cli(self):
        """
        Main command-line interface function.
        :return: No return value
        """
        left_file: str = ""
        right_file: str = ""
        opt_length: int = len(self.options)

        if opt_length == 0:
            self.invoke_application(left_file, right_file)
            return
        elif opt_length == 1 and self.options[0] == "--help":
            if self.options[0] == "--help":
                self.help_func()
            elif self.options[0] == "--about":
                self.about_func()
        elif opt_length == 2:
            if utilities.check_paths(self.options[0], self.options[1]):
                left_file = self.options[0]
                right_file = self.options[1]
            elif self.options[0] == "--file":
                print("Error: 2 files required for comparison.")
        elif opt_length == 3 and self.options[0] == "--file" and utilities.check_paths(self.options[1], self.options[2]):
            left_file = self.options[1]
            right_file = self.options[2]
        elif opt_length == 4 and \
                self.options[0] == "--file" and \
                self.options[2] == "--file" and \
                utilities.check_paths(self.options[1], self.options[3]):
            left_file = self.options[1]
            right_file = self.options[3]
        else:
            print("Error: Invalid options. Type '--help' for information.")
            return

        self.invoke_application(left_file, right_file)

    @staticmethod
    def help_func():
        print(
            """
------------------------------------------------------------
PyMerge
------------------------------------------------------------
    --file: File to compare.\n\tUsage: '[--file] <left_file> <right_file>'
    --help: Show command line options.\n\tUsage: '[--help]'
    --about: Link to the PyMerge project README. \n\n
            """
        )

    @staticmethod
    def about_func():
        print(
            "The PyMerge project page can be found here: https://github.com/WSU-4110/PyMerge/blob/master/README.md\n"
        )

    @staticmethod
    def sanitize(options: list or set) -> list or set:
        """
        Santizes raw user input to something that can be used without error.
        :param options: list of options provided by user.
        :return:
        """
        sanitized: list = []
        file_options: set = {"--f", "-file", "-f"}
        help_options: set = {"--h", "-h", "--he", "-he", "--hel", "-hel", "--help", "-help"}
        about_options: set = {"--about", "-about", "--abot", "-abot", "--abut", "-abut", "--abt", "-abt", "--info",
                              "-info"}

        for n in range(len(options)):
            options[n] = str(options[n].replace(" ", ""))
            option_lower: str = options[n].lower()

            if option_lower == " " or options[n] == "":
                continue
            elif option_lower in file_options:
                sanitized.append("--file")
            elif option_lower in help_options:
                sanitized.append("--help")
            elif option_lower in about_options:
                sanitized.append("--about")
            else:
                sanitized.append(options[n])

        return sanitized

    def invoke_application(self, file1: str, file2: str):
        """Invoke the main application here"""

        if file1 != "" or file2 != "":
            if self.validate_files(file1, file2, path_check=False):
                MainWindow.start_main(file1, file2)
        else:
            MainWindow.start_main()
        print(file1, file2)

    def validate_files(self, file1, file2, path_check=False):
        size_valid = utilities.validate_file_size(file2, self.file_size_lim) and \
                     utilities.validate_file_size(file2, self.file_size_lim)
        ext_valid = utilities.valid_file_ext(file1) and utilities.valid_file_ext(file2)
        paths_valid = utilities.check_paths(file1, file2) if path_check else True

        if size_valid and ext_valid and paths_valid:
            return True


if __name__ == '__main__':
    PyMergeCLI(sys.argv)
