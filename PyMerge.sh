#!/bin/bash
###########################################################################
# File: PyMerge.sh
# Author: Malcolm Hall
# Description: Main start script for PyMerge. This checks for a valid Python installation
#              and calls the main Python file (PyMerge.py).
#
#
# Copyright (C) PyMerge Team 2019
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
###########################################################################

invocation_file=PyMerge.py  # Default main Python file
invocation_file_final=""  # Verified main Python file
leftfile=$1 # Possible left file to compare (first argument)
rightfile=$2 # Possible right file to compare (second argument)
python_vld=false  # Indicates if there is a valid Python installation
python3_exec=""  # Python executable to call

# These are the valid Python versions to run PyMerge with
declare -a python_versions=("python3.5" "python3.6" "python3.7" "python3.8" "python3.9")

# Check for Python 3.5+ by looping through the array of accepted Python versions.
# This is done to make it easier to update the list of accepted versions
for version in "${python_versions[@]}"
do
  if command -v "$version" &>/dev/null; then
    python3_exec="$version"  # Set the Python version we'll use to start the progam
    python_vld=true # Set the flag indicating that there is a valid Python version installed
    echo "python3 requirement satisfied, using $python3_exec"
    break
  fi
done

if [ "$python_vld" == true ]; then
  : # Do nothing
else
  echo "python3_exec not found! Please install Python 3.5+ before running PyMerge."
  exit 0
fi


# In git repository, PyMerge.sh and PyMerge.bat are in the same directory as
# the Python files being called. In the installed version, PyMerge.sh and PyMerge.bat
# located one directory above the Python files so both paths need to be checked.
if test -f "$invocation_file"; then
  invocation_file_final="$invocation_file"
elif test -f "../$invocation_file"; then
  invocation_file_final="../$invocation_file"
else
  echo "Could not find PyMerge.py! Exiting..."
  exit 0
fi

"$python3_exec" "$invocation_file_final" "$leftfile" "$rightfile"
