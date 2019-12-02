#Installing PyMerge

## Using BitRock InstallBuilder
If you have a valid BitRock InstallBuilder license, you can use the configuration file found
in this directory to create custom installation files. 

The InstallBuilder configuration file, PyMerge_Installer.xml, is located in this directory and
can be loaded into InstallBuilder to create custom installation programs. The  file paths in
PyMerge_Installer.xml may need to be changed to reflect those on your machine.

## Installation files
Executable installers are included for macOS, Windows, and Linux.

## How to install PyMerge
Download the appropriate installer for PyMerge.

| OS            | Architecture | Installer     |
| :---          |    :----:    |          :--- |
| **Windows**   | x64          | PyMerge-1.0-windows-x64-installer.exe   |
| **Windows**   | x86          | PyMerge-1.0-windows-installer.exe      |
| **macOS**     | --           | PyMerge-1.0-osx-installer               |
| **Linux**     | x64          | PyMerge-1.0-linux-x64-installer.run     |
| **Linux**     | x86          | PyMerge-1.0-linux-installer.run         |

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
