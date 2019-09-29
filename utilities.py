"""
utilities.py

General, non-project-specific functions

"""


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



