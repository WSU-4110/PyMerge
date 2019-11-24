from unittest import TestCase
import file_backup
import hashlib
import os


class TestBackup(TestCase):
    def setUp(self) -> None:
        self.backup = file_backup.Backup()


class TestInit(TestBackup):
    def test_initial_block_size(self):
        self.assertEqual(self.backup.BLOCK_SIZE, 65535)
        self.assertNotEqual(self.backup.BLOCK_SIZE, 0)
        self.assertAlmostEqual(self.backup.BLOCK_SIZE, 65534)

    def test_initial_hash_type(self):
        self.assertEqual(self.backup.hash_type, "SHA256")
        self.assertNotEqual(self.backup.hash_type, "SHA224")
        self.assertNotEqual(self.backup.hash_type, "SHA512")
        self.assertNotEqual(self.backup.hash_type, "MD5")

    def test_initial_hash_func(self):
        self.assertEqual(self.backup.hash_func, hashlib.sha256)
        self.assertNotEqual(self.backup.hash_func, hashlib.sha224)
        self.assertNotEqual(self.backup.hash_func, hashlib.sha512)
        self.assertNotEqual(self.backup.hash_func, hashlib.md5)


class TestMethods(TestBackup):
    def test_get_hash_func(self):
        self.assertEqual(self.backup.get_hash_func("SHA256"), hashlib.sha256)
        self.assertEqual(self.backup.get_hash_func("SHA224"), hashlib.sha224)
        self.assertEqual(self.backup.get_hash_func("SHA512"), hashlib.sha512)
        self.assertEqual(self.backup.get_hash_func("MD5"), hashlib.md5)
        self.assertEqual(self.backup.get_hash_func("SHA128"), hashlib.sha256)
        self.assertEqual(self.backup.get_hash_func(""), hashlib.sha256)
        self.assertEqual(self.backup.get_hash_func("SHA1"), hashlib.sha256)

    def test_format_datetime(self):
        self.assertEqual(self.backup.format_datetime("2019-11-24 15:19:15.066975"), "20191124_151915066975")
        self.assertNotEqual(self.backup.format_datetime("2019-11-24 15:19:15.066975"), "")
        self.assertEqual(self.backup.format_datetime("2000-1-24 15:19:15.066975"), "2000124_151915066975")
        self.assertEqual(self.backup.format_datetime(" "), "_")
        self.assertEqual(self.backup.format_datetime(""), "")
        self.assertNotEqual(self.backup.format_datetime(" "), " ")

    def test_check_for_backup_folder(self):
        self.backup.check_for_backup_folder()
        self.assertEqual(os.path.exists("backup"), True)
        os.rmdir("backup")
        self.assertEqual(os.path.exists("backup"), False)

    def test_get_meta_file_name(self):
        self.assertEqual(self.backup.get_meta_file_name("test.c"), ".meta.test.c.dat")
        self.assertEqual(self.backup.get_meta_file_name(""), ".meta..dat")
        self.assertEqual(self.backup.get_meta_file_name("   "), ".meta.   .dat")
        self.assertNotEqual(self.backup.get_meta_file_name("test.c"), "test.c")
        self.assertNotEqual(self.backup.get_meta_file_name("test.c"), ".meta.test.dat")
        self.assertNotEqual(self.backup.get_meta_file_name("test.c"), "test.c.dat")

    # def test_get_hash(self):
    #     self.fail()

    def test_get_hash_file_name(self):
        self.assertEqual(self.backup.get_hash_file_name("SHA256"), "SHA256.txt")
        self.assertEqual(self.backup.get_hash_file_name("SHA224"), "SHA224.txt")
        self.assertEqual(self.backup.get_hash_file_name("SHA512"), "SHA512.txt")
        self.assertEqual(self.backup.get_hash_file_name("MD5"), "MD5.txt")
        self.assertEqual(self.backup.get_hash_file_name(""), ".txt")
        self.assertEqual(self.backup.get_hash_file_name("TEST"), "TEST.txt")
        self.assertEqual(self.backup.get_hash_file_name(" "), " .txt")
