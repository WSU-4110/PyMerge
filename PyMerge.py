"""
This is the entry point for the PyMerge program. Command line arguments will be passed
to this file and the functions in this file will invoke the GUI. There will be no merge/compare/GUI
algorithms in this file. It will only call the main GUI and application functions.

"""

import sys
import os

# import FileCompareTable
import mainWindow


class PyMergeCLI(object):
    error_msgs = {
        "FILE_CNT": "Exactly two files must be specified to compare/merge.",
        "FILE_DNE": "File does not exist: ",
    }

    def __init__(self, *args):
        self.options = self.sanitize(args[0][1:])
        self.cli()

    def cli(self):
        left_file = ""
        right_file = ""

        if len(self.options) == 0:
            self.invoke_application(left_file, right_file)
            return
        elif len(self.options) == 2 and self.check_paths(
            self.options[0], self.options[1]
        ):
            left_file = self.options[0]
            right_file = self.options[1]
        elif (
            len(self.options) == 3
            and self.options[0] == "--file"
            and self.check_paths(self.options[1], self.options[2])
        ):
            left_file = self.options[1]
            right_file = self.options[2]
        elif (
            len(self.options) == 4
            and self.options[0] == "--file"
            and self.options[2] == "--file"
            and self.check_paths(self.options[1], self.options[3])
        ):
            left_file = self.options[1]
            right_file = self.options[3]
        elif len(self.options) == 1 and self.options[0] == "--help":
            self.help_func()
        elif len(self.options) == 1 and self.options[0] == "--about":
            self.about_func()
        else:
            print("Invalid options. Type '--help' for information.")
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
        sanitized: list = []
        file_options: set = {"--f", "-file", "-f"}
        help_options: set = {
            "--h",
            "-h",
            "--he",
            "-he",
            "--hel",
            "-hel",
            "--help",
            "-help",
        }
        about_options: set = {
            "--about",
            "-about",
            "--abot",
            "-abot",
            "--abut",
            "-abut",
            "--abt",
            "-abt",
            "--info",
            "-info",
        }

        for n in range(len(options)):
            options[n] = str(options[n].replace(" ", ""))

            if options[n] == " " or options[n] == "":
                continue
            elif options[n].lower() in file_options:
                sanitized.append("--file")
            elif options[n].lower() in help_options:
                sanitized.append("--help")
            elif options[n].lower() in about_options:
                sanitized.append("--about")
            else:
                sanitized.append(options[n])

        return sanitized

    @staticmethod
    def invoke_application(file1, file2):
        # """Invoke the main application here"""
        # if len(sys.argv) == 4:
        #     mainWindow.startMain(file1, file2)
        # else:
        #     mainWindow.startMain()
        print(file1, file2)

    @staticmethod
    def check_paths(*args):
        for arg in args:
            if not os.path.exists(arg) or not os.path.isfile(arg):
                print("Invalid file path: ", arg)
                return False
        return True


if __name__ == "__main__":
    PyMergeCLI(sys.argv)
