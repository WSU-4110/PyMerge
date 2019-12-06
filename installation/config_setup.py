"""
###########################################################################
File: config_setup.py
Author: Malcolm Hall
Description: Updates the installer configuration file


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


import argparse
import pathlib
import os
import re

"""
Functionality:
    1. Update all paths
        a. change all paths to relative paths (default) or
        b. change all paths to absolute paths for the machine its on
    2. Update the PyMerge version given in the installer file
    3. Change README.md file path
    4. Change the license file path
    5. Change the splash image path
"""


def cfg_setup():
    cfg_file_vld = False
    license_file_vld = False
    readme_file_vld = False
    curr_version = None

    parser = argparse.ArgumentParser(description="Installer configuration setup script.")
    parser.add_argument("-file", type=str, help="Installer config file to setup.")
    parser.add_argument("-splash", type=str, help="Set the splash image file.")
    parser.add_argument("-license", type=str, help="Set the license file.")
    parser.add_argument("-readme", type=str, help="Set the readme file.")
    parser.add_argument("-version", type=str, help="Set the PyMerge version.")
    args = parser.parse_args()

    if args.file is not None:
        cfg_file_vld = os.path.isfile(args.file)
    if args.license is not None:
        license_file_vld = os.path.isfile(args.license)
    if args.readme is not None:
        readme_file_vld = os.path.isfile(args.readme)

    if cfg_file_vld:
        with open(args.file, 'r') as file:
            cfg_contents = file.read()

            if args.version is not None:
                version_re = re.compile("<version>[0-9.0-9]*</version>")
                version_info = version_re.findall(cfg_contents)

                if len(version_info) > 0:
                    cfg_contents.replace(version_info[0], f"<version>{args.version}</version>")

            if license_file_vld or True:
                license_re = re.compile("<licenseFile>.*</licenseFile>")
                license_info = license_re.findall(cfg_contents)

                if len(license_info) > 0:
                    cfg_contents.replace(license_info[0], f"<licenseFile>{args.license}</licenseFile>")

            if readme_file_vld or True:
                readme_re = re.compile("<readmeFile>.*</readmeFile>")
                readme_info = license_re.findall(cfg_contents)

                if len(readme_info) > 0:
                    cfg_contents.replace(readme_info[0], f"<readmeFile>{args.readme}</readmeFile>")


cfg_setup()