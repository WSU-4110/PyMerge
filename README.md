![logo](icons/InstallerSplash.png "PyMerge Splash")
## PyMerge is a diff/merge utility written in Python, enabling seamless, cross-platform use.

### Installation
#### System Requirements:
Although PyMerge should run on most machines with Python 3.7+ installed, for best performance your computer should have
the specifications listed below:

* Minimum recommended machine specifications:
    * Dual core processor, 2.5GHz
    * 2GB Ram
    * [Python 3.7+](https://www.python.org/downloads/)
    * OS:
        * Windows 7 or later
        * macOS 10.9 or later
        * Linux
#### Option 1: Installer:
Download the appropriate installer for PyMerge.

| OS            | Architecture| Installer     |
| :---          |    :----:   |          :--- |
| **Windows**   | x64         | [PyMerge-1.0-windows-x64-installer.exe]()   |
| **Windows**   | x86         | [PyMerge-1.0-windows-installer.exe]()       |
| **macOS**     | --          | [PyMerge-1.0-osx-installer]()               |
| **Linux**     | x64         | [PyMerge-1.0-linux-x64-installer.run]()     |
| **Linux**     | x86         | [PyMerge-1.0-linux-installer.run]()         |

#### Option 2: Clone the repository
You may optionally clone the repository and just run PyMerge.py directly (this is the more 
portable way of doing things) from your command line. 

#### Dependencies
For the most part, PyMerge uses native Python modules. The exceptions to this are when the
Cython extensions need to be generated. The installer includes Cython modules for Linux, Windows, or macOS, 
but on occasion, new object files will need to be compiled. This can be done by navigating
to the cython_accelerator folder in the main application folder and running the following 
in terminal/command-line:
~~~~
python3 setup.py build_ext --inplace
~~~~

In the event that something goes wrong with compiling the object file, PyMerge will automatically
use the Python versions of the file diff algorithms it has implemented.

### Use
#### Command line usage:
In your terminal, type 
~~~~~
python3 PyMerge.py <file1> <file2>
~~~~~
Where \<file1\> is the file you would like to appear on the left-hand side of the comparison window and
\<file2\> is the file you would like to appear on the right-hand side.
This will start the application and load the comparison table for the two files passed as arguments.

For example:
~~~~~
python3 PyMerge.py myFile1.txt myFile2.txt
~~~~~


Alternatively, you may start the application without any arguments and load the files: later:
~~~~~
python3 PyMerge.py
~~~~~

#### Running with invocation script/executable:
Each installation includes a script or executable meant to invoke the main program. For macOS and Linux this 
will be a bash file (.sh) or a binary. For Windows this will be a batch file (.bat) or a binary. Double clicking
these files will run the main PyMerge application. No files will be loaded this way, so you must select the 
file you would like to compare after the program initializes. 

#### Merging a file
Once two files have been loaded into the comparison table and PyMerge has finished analyzing the files
, the differences between the two files will be displayed using color codes. Red indicates that two
lines are different between the two files. Dark gray indicates that lines have been added in the other 
file. Light green/mint or white indicates that the lines are the same. 

To merge a line, press the array button in the center of the comparison table. The text will merge
from one side, to the side that the arrow is pointing to. The line will then change its background
color to a light blue to indicate that a merge has occurred. 

####Undo/Redo
Accidents happen. To undo or redo a merge, press the curved arrow buttons on the top toolbar,
or press the 'Ctrl+Z' and 'Ctrl+Y' hot-keys. This will restore the state to what it was 
before the last merge event.

#### Saving a file
Once you have finished merging the two files, you can save the files using File->Save. 
A backup of your original file will be created and the newly merged changes will be 
written to the original file. The changes are written in-place because creating a
new file would likely cause issues with any version control tools being used to track
the two files. Merging in-place removes the possibility that the VCS will recognize the
files as new rather than changed.

#### Retrieving a backup
In the event that a file is saved accidentally, the original data is not lost. Backups of 
the original files are saved to a folder called 'backups' in the main application folder. 
Find the correct backup file (they have the same name as the original but with .bak appended
onto the end), write click, and extract using your preferred compression utility. These
backup files are just ZIP archives.

### Acknowledgements
#### Icons
* add.png: 
* down-arrow.png:
* up-arrow.png:
* left-arrow.png: 
* right-arrow.png:
* undo-arrow.png:
* redo-arrow.png:

#### Installer builder:
* BitRock InstallBuilder Enterprise 19.8.0 \
![logo](icons/installersby_tiny.png "Installers by BitRock")