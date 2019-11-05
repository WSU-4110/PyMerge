"""
utilities.py
General, non-project-specific functions
"""
import hashlib
import os
import sys

from PyQt5.QtWidgets import *


def pad_string(string: str, length: int, char=" ", append=True):
    """
    Pad a string with a specified character. Defaults to " " and appending to end.
    :param string: string to pad
    :param length: desired string length
    :param char: character to pad with
    :param append: add padding to front or back of string
    :return: padded string
    """
    if append:
        return string + (char * (len(string) - int(length)))
    else:
        return (char * (len(string) - int(length))) + string


def file_writable(file: str) -> bool:
    """
    Checks if a file has write permissions.
    :param file: path to file
    :return: boolean indicating if a file has write permissions or not.
    """
    return os.access(file, os.W_OK)


def file_readable(file: str) -> bool:
    """
    Checks if a file as read permissions.
    :param file: path to file
    :return: boolean indicating if file has read permissions or not
    """
    return os.access(file, os.R_OK)


def hamming_dist(string1: str, string2: str) -> int or None:
    """
    Calculates the Hamming distance of two strings. Can be used for finding minor changes between two strings.
    :param string1: string to compare
    :param string2: string to compare
    :return: Integer indicating hamming distance or None if the strings are not equal length.
    """
    string1_len = len(string1)
    string2_len = len(string2)

    if string1_len == string2_len:
        return sum([string1[n] != string2[n] for n in range(string1_len)])
    else:
        return None


def line_bit_vector(string1, string2) -> list:
    """
    Calculates a bit vector to indicate differences between two lines.
    Does not calculate edit scripts or edit distance.
    :param string1:
    :param string2:
    :return:
    """
    string1_len = len(string1)
    string2_len = len(string2)
    max_len = max(string1_len, string2_len)
    bit_vec = [0] * max_len

    for n in range(max_len):
        try:
            bit_vec[n] = int(not (string1[n] == string2[n]))
        except IndexError:
            bit_vec[n] = 1
    return bit_vec


def hash_list(inp_list):
    for n in range(inp_list):
        inp_list[n] = hashlib.md5(str(inp_list[n]).encode("utf-8"))

    return


# @staticmethod
def valid_file_ext(file: str) -> bool:
    illegal_exts = {"zip", "bzip", "mp3", "wav", "jpg", "png", "mp4", "ppt", "ods", "tar", "wma", "aif", "m4a",
                    "mpg", "vob", "wmv", "obj", "gif", "tiff", "3dm", "3ds", "svg", "xls", "xlsx", "7z", "",
                    "gz", "iso", "bin", "msi", "docx"}
    file_ext = file.split('.')[-1]

    if file_ext in illegal_exts:
        print(f"Error: {file} is not an accepted format.")
        return False
    else:
        return True


def validate_file_size(file: str, file_size_lim: int) -> bool:
    """
    Validate the size of a file according to a limit parameter
    :param file: File to be checked
    :param size_lim: size limit in bytes
    :return: boolean indicating whether file is below size limit
    """
    if os.stat(file).st_size > file_size_lim:
        print(f"Error: {file} is greater than limit of {file_size_lim} bytes")
        return False
    else:
        return True


# @staticmethod
def check_paths(*args):
    for arg in args:
        try:
            if not os.path.exists(arg) or not os.path.isfile(arg):
                print("Invalid file path: ", arg)
                return False
        except (FileNotFoundError, FileExistsError):
            return False
    return True
def hashing(ilist):
    olist=list()
    for string in ilist:
        olist.append(int(hashlib.md5(string.encode()).hexdigest(),16))
    return olist
def error(self):
    QmessageBox.critical(self,"Error","There was an error")