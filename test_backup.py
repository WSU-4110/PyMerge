"""
###########################################################################
File:
Author:
Description:


Copyright (C) 2019

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

import hashlib
import os
from unittest import TestCase

import file_backup


class TestBackup(TestCase):
    def setUp(self) -> None:
        self.backup = file_backup.Backup()


class TestInit(TestBackup):
    def test_initial_block_size(self):
        self.assertEqual(self.backup.BLOCK_SIZE, 65535)
        self.assertNotEqual(self.backup.BLOCK_SIZE, 0)

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
        self.assertEqual(os.path.exists("backup"), False)
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

    def test_get_hash(self):
        open("hash_test.txt", 'w+').close()
        self.backup.hash_func = self.backup.get_hash_func("SHA256")
        self.assertEqual(self.backup.get_hash("hash_test.txt"), "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
        self.backup.hash_func = self.backup.get_hash_func("MD5")
        self.assertEqual(self.backup.get_hash("hash_test.txt"), "d41d8cd98f00b204e9800998ecf8427e")
        self.backup.hash_func = self.backup.get_hash_func("SHA224")
        self.assertEqual(self.backup.get_hash("hash_test.txt"), "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f")
        self.backup.hash_func = self.backup.get_hash_func("SHA512")
        self.assertEqual(self.backup.get_hash("hash_test.txt"), "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e")
        os.remove("hash_test.txt")

    def test_get_hash_file_name(self):
        self.assertEqual(self.backup.get_hash_file_name("SHA256"), "SHA256.txt")
        self.assertEqual(self.backup.get_hash_file_name("SHA224"), "SHA224.txt")
        self.assertEqual(self.backup.get_hash_file_name("SHA512"), "SHA512.txt")
        self.assertEqual(self.backup.get_hash_file_name("MD5"), "MD5.txt")
        self.assertEqual(self.backup.get_hash_file_name(""), ".txt")
        self.assertEqual(self.backup.get_hash_file_name("TEST"), "TEST.txt")
        self.assertEqual(self.backup.get_hash_file_name(" "), " .txt")
