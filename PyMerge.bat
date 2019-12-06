<<<<<<< HEAD
::!/bin/bash
::##########################################################################
:: File: PyMerge.sh
:: Author: Malcolm Hall
:: Description: Main start script for PyMerge. This checks for a valid Python installation
::              and calls the main Python file (PyMerge.py).
::
::
:: Copyright (C) PyMerge Team 2019
::
:: This program is free software: you can redistribute it and/or modify
:: it under the terms of the GNU General Public License as published by
:: the Free Software Foundation, either version 3 of the License, or
:: (at your option) any later version.
::
:: This program is distributed in the hope that it will be useful,
:: but WITHOUT ANY WARRANTY; without even the implied warranty of
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
:: GNU General Public License for more details.
::
:: You should have received a copy of the GNU General Public License
:: along with this program.  If not, see <https://www.gnu.org/licenses/>.
::##########################################################################

@echo off
:: Default main Python file
SET invocation_file=PyMerge.py  
:: Verified main Python file
SET invocation_file_final=""  
:: Possible left file to compare (first argument)
SET leftfile=1 
:: Possible right file to compare (second argument)
SET rightfile=2 
:: Indicates if there is a valid Python installation
SET python_vld=false 
:: Python executable to call 
SET python3_exec=""  
:: These are the valid Python versions to run PyMerge with
SET python_versions=python3.5 python3.6 python3.7 python3.8 python3.9

cd app

for %%v in (%python_versions%) do (
  if ... (
    :: Set the Python version we'll use to start the progam
    %python3_exec%=%%v  
    :: Set the flag indicating that there is a valid Python version installed
    %python_vld%=True 
    echo python3 requirement satisfied, using $python3_exec%
    break
  )
)

if %python_vld% == False (
  echo python3_exec not found! Please install Python 3.5+ before running PyMerge.
  exit 0
)

:: In git repository, PyMerge.sh and PyMerge.bat are in the same directory as
:: the Python files being called. In the installed version, PyMerge.sh is located
:: inside the /app/ folder so the path to PyMerge.py needs to be set accordingly.
if exist %invocation_file% (
  invocation_file_final=%invocation_file%
) else if exist ../%invocation_file% (
  invocation_file_final=../%invocation_file%
) else if exist app/%invocation_file% (
  invocation_file_final=app/%invocation_file%
) else (
  echo Could not find PyMerge.py! Exiting...
  exit 0
)

=======
python3 PyMerge.py
>>>>>>> 98e19d2129e5fb9c4f672af457ff3d14070a462c
