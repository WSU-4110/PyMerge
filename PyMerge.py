"""
This is the entry point for the PyMerge program. Command line arguments will be passed
to this file and the functions in this file will invoke the GUI. There will be no merge/compare/GUI
algorithms in this file. It will only call the main GUI and application functions.

"""

import sys
import os
#import FileCompareTable
import mainWindow

class PyMergeCLI(object):

    help_values = {
        "-file": "File to compare.\n\tUsage: '-file <file_name>'",
        "-help": "Show command line options.\n\tUsage: '-help'",
        "-about": "Credits and information about PyMerge.",
    }

    error_msgs = {
        "FILE_CNT": "Exactly two files must be specified to compare/merge.",
        "FILE_DNE": "File does not exist: ",
    }

    def __init__(self, *args):
        self.options = args[0][1:]
        self.cli(self.options)

    def cli(self, options):
        left_file = None
        right_file = None

        if len(options) == 0:
            self.invoke_application("", "")

        for idx, opt in enumerate(options):
            if self.resolve_option(opt) == "--file" and len(options) == 4:
                if left_file is None:
                    if os.path.exists(options[idx + 1]) and os.path.isfile(options[idx + 1]):
                        left_file = options[idx + 1]
                    else:
                        print(self.error_msgs["FILE_DNE"] + options[idx + 1])
                        return

                elif left_file is not None and right_file is None:
                    if os.path.exists(options[idx + 1]) and os.path.isfile(options[idx + 1]):
                        right_file = options[idx + 1]
                    else:
                        print(self.error_msgs["FILE_DNE"] + options[idx + 1])
                        return
                else:
                    print(self.error_msgs["FILE_CNT"])
                    return

            elif self.resolve_option(opt) == "--help" and len(options) == 1:
                for key in self.help_values:
                    print(key + " : " + self.help_values[key])

            else:
                print("Invalid options. Enter '--help' for more information.")
                return

        if len(options) == 4 and left_file is not None and right_file is not None:
            self.invoke_application(left_file, right_file)


    @staticmethod
    def resolve_option(option):
        file_options = {"--f", "-file"}
        help_options = {"--h", "-h", "--he", "-he", "--hel", "-hel", "--help", "-help"}
        about_options = {"--about", "-about", "--abot", "-abot", "--abut", "-abut", "--abt", "-abt", "--info", "-info"}

        if option.lower() in file_options:
            return "--file"
        elif option.lower() in help_options:
            return "--help"
        elif option.lower() in about_options:
            return "--about"
        else:
            return option

    def invoke_application(self, file1, file2):
        """Invoke the main application here"""
        
        if len(sys.argv) == 3:
            mainWindow.startMain( file1, file2 )
        else:
            mainWindow.startMain()
        


if __name__ == '__main__':
    PyMergeCLI(sys.argv)
