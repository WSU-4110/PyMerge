import zipfile
import hashlib
import os


class Backup(object):
    def __init__(self, hash="SHA256"):
        self.history: list = []
        self.BLOCK_SIZE: int = 65535
        self.hash_type: str = hash
        self.hash_func = hashlib.sha256()

    def get_hash(self, file: str) -> hex:
        """
        Calculates the hash value for a file
        :param file: file to get hash for
        :return: hex digest version of hash
        """
        if self.hash_type == "SHA224":
            self.hash_func = hashlib.sha224()
        if self.hash_type == "SHA256":
            self.hash_func = hashlib.sha256()
        if self.hash_type == "SHA512":
            self.hash_func = hashlib.sha512()
        if self.hash_type == "MD5":
            self.hash_func = hashlib.md5()

        with open(file, 'rb') as in_file:
            file_buf = in_file.read(self.BLOCK_SIZE)

            while len(file_buf) > 0:
                self.hash_func.update(file_buf)
                file_buf = in_file.read(self.BLOCK_SIZE)

        #print(self.hash_func.hexdigest())
        return self.hash_func.hexdigest()

    def check_hash(self, file, hash_value: str) -> bool:
        """
        Checks the validity of a hash value against the calculates hash for a file
        :param file:
        :param hash_value:
        :return: boolean indicating file integrity
        """
        return hash_value == self.get_hash(file)

    def create_backup(self, file: str) -> str:
        """
        Creates a zip archive containing a backup of a file and the hash value
        :param file: file to be backed up
        :return: absolute path to backup
        """
        hash_file = f"{self.hash_type}.txt"
        with open(hash_file, 'w+') as temp:
            temp.write(str(self.get_hash(file)))

        with zipfile.ZipFile(f"{file}.bak.zip", 'w', zipfile.ZIP_DEFLATED) as backup:
            backup.write(file)
            backup.write(hash_file)

        return os.path.abspath(f"{file}.bak.zip")

    def retrieve_backup(self, backup_file, file_name):
        """
        Function to retrieve the backup file from the zip archive. Checks the hash value for integrity
        :param backup_file: backup file to extract
        :param file_name: file to be backed up
        :return:
        """
        with zipfile.ZipFile(backup_file) as myzip:
            myzip.extract(file_name)
            myzip.extract(f"{self.hash_type}.txt")

        with open(f"{self.hash_type}.txt", 'r') as hash_file:
            hash_string = hash_file.read().strip('\n')

        if not self.check_hash(backup_file.strip(".bak.zip"), hash_string):
            os.remove(file_name)
        os.remove(f"{self.hash_type}.txt")



def test():
    test  = Backup()
    backup = test.create_backup("file1.c")
    os.remove("file1.c")
    test.retrieve_backup(backup, "file1.c")