from enum import Enum, unique, auto

import pmEnums
import file_backup

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


class MergeFinalizer(object):
    def __init__(self, outp_file_left: str, outp_file_right: str):
        self.outp_file_left = outp_file_left
        self.outp_file_right = outp_file_right
        self.backup = file_backup.Backup()

    @staticmethod
    def type_checker(data_set: list or set, target_type: type) -> Status:
        for item in data_set:
            if not isinstance(item, target_type):
                return Status.TYPE_CHK_ERROR
        return Status.TYPE_CHK_SUCCESS

    @staticmethod
    def deletion(data_set: list or set, output_set: list or set, delete_token=None) -> Status:
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
        try:
            self.backup.create_backup(self.outp_file)
        except:
            return Status.BACKUP_ERROR
        return Status.BACKUP_ERROR

    def finalize_merge(self, left_set, right_set):
        outp_set_left = []
        outp_set_right = []

        if self.type_checker(left_set, target_type=str) == Status.TYPE_CHK_SUCCESS and self.type_checker(right_set, target_type=str) == Status.TYPE_CHK_SUCCESS:
            if self.deletion(left_set, outp_set_left) == Status.DELETE_SUCCESS and self.deletion(right_set, outp_set_right) == Status.DELETE_SUCCESS:
                if self.backup_file() == Status.BACKUP_SUCCESS:
                    try:
                        with open(self.outp_file_left, 'w') as file:
                            file.truncate(0)
                            for line in outp_set_left:
                                file.write(line)
                    except (FileExistsError, FileNotFoundError):
                        return Status.FILE_WRITE_ERROR
                    try:
                        with open(self.outp_file_right, 'w') as file:
                            file.truncate(0)
                            for line in outp_set_right:
                                file.write(line)
                    except (FileExistsError, FileNotFoundError):
                        return Status.FILE_WRITE_ERROR
                else:
                    return Status.BACKUP_ERROR
            else:
                return Status.DELETE_ERROR
        else:
            return Status.TYPE_CHK_ERROR

