from enum import Enum, unique

import file_backup
import utilities
import os

"""
Get data from table -> type checking -> deletions -> original file backup -> truncate file -> write data to file
-> close file -> alert user (to be handled in frontend)
"""


@unique
class Status(Enum):
    DATA_RETRV_SUCCESS = 0
    DATA_RETRV_ERROR = 1
    TYPE_CHK_SUCCESS = 2
    TYPE_CHK_ERROR = 3
    DELETE_SUCCESS = 4
    DELETE_ERROR = 5
    BACKUP_SUCCESS = 6
    BACKUP_ERROR = 7
    TRUNC_SUCCESS = 8
    TRUNC_ERROR = 9
    FILE_WRITE_SUCCESS = 10
    FILE_WRITE_ERROR = 11
    FILE_PERMISSION_ERR = 12
    MERGE_FINALIZE_SUCCESS = 13


class MergeFinalizer(object):
    def __init__(self, outp_file_left: str, outp_file_right: str, backup_dir: str):
        self.outp_file_left: str = outp_file_left
        self.outp_file_right: str = outp_file_right
        self.backup = file_backup.Backup()
        self.backup_dir = backup_dir

    @staticmethod
    def check_for_backup_dir():
        try:
            if os.path.exists("file_backup") and os.path.isdir("file_backup"):
                return True
            else:
                os.mkdir("file_backup")
                return True
        except OSError:
            return False

    @staticmethod
    def type_checker(data_set: list or set, target_type: type) -> Status:
        """
        Checks the type of every item in the list or set against the provided target type.

        :param data_set: Set to check
        :param target_type: Type to check for
        :return: enumerated Status value
        """
        for item in data_set:
            if not isinstance(item, target_type) and item is not None:
                return Status.TYPE_CHK_ERROR
        return Status.TYPE_CHK_SUCCESS

    @staticmethod
    def set_equal(left_set: set or list or tuple, right_set: set or list or tuple) -> bool:
        """
        Returns whether two sets or lists are equal
        """
        return left_set == right_set

    @staticmethod
    def deletion(
        data_set: list or set, output_set: list or set, delete_token=None
    ) -> Status:
        """
        Takes an input list or set and adds every item that does not equal the delete token to the
        output list.

        :param data_set: Set or list to check
        :param output_set: Set to add items from input list to
        :param delete_token: Item to check for
        :return: Status enumeration
        """
        for item in data_set:
            try:
                if delete_token is None:
                    if item is not None:
                        output_set.append(item)
                else:
                    if item != delete_token:
                        output_set.append(item)
            except:
                return Status.DELETE_ERROR
        return Status.DELETE_SUCCESS

    def backup_file(self) -> Status:
        """

        :return:
        """
        try:
            self.backup.create_backup(f"{self.outp_file_left}", self.backup_dir)
            self.backup.create_backup(f"{self.outp_file_right}", self.backup_dir)
        except Exception as ex:
            print(ex)
            return Status.BACKUP_ERROR
        return Status.BACKUP_SUCCESS

    def finalize_merge(self, left_set: list or set, right_set: list or set) -> Status:
        """

        :param left_set:
        :param right_set:
        :return:
        """
        outp_set_left: list = []
        outp_set_right: list = []

        self.check_for_backup_dir()

        if not utilities.file_writable(self.outp_file_left) or not utilities.file_writable(self.outp_file_right):
            return Status.FILE_PERMISSION_ERR

        elif (
            self.type_checker(left_set, target_type=str) != Status.TYPE_CHK_SUCCESS
            or self.type_checker(right_set, target_type=str) != Status.TYPE_CHK_SUCCESS
        ):
            return Status.TYPE_CHK_ERROR

        elif (
            self.deletion(left_set, outp_set_left) != Status.DELETE_SUCCESS
            or self.deletion(right_set, outp_set_right) != Status.DELETE_SUCCESS
        ):
            return Status.DELETE_ERROR

        elif self.backup_file() != Status.BACKUP_SUCCESS:
            return Status.BACKUP_ERROR
        else:
            try:
                with open(self.outp_file_left, "w") as file:
                    for line in outp_set_left:
                        file.write(line)
                        if "\n" not in line:
                            file.write("\n")
            except (FileExistsError, FileNotFoundError):
                return Status.FILE_WRITE_ERROR
            try:
                with open(self.outp_file_right, "w") as file:
                    for line in outp_set_right:
                        file.write(line)
                        if "\n" not in line:
                            file.write("\n")
            except (FileExistsError, FileNotFoundError):
                return Status.FILE_WRITE_ERROR

        return Status.MERGE_FINALIZE_SUCCESS