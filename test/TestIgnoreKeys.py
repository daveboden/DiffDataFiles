import unittest
import DiffDataFiles

filename = "ignore-keys-test-file.txt"

class TestStringMethods(unittest.TestCase):

    def test_read(self):
        lines = DiffDataFiles.read_keys_file_into_array(filename)
        self.assertEqual(['AAA', 'BBB', 'CCC'], lines)
        print lines
        self.assertTrue(DiffDataFiles.should_key_be_ignored(lines, "AAA"))
        self.assertFalse(DiffDataFiles.should_key_be_ignored(lines, "JJJ"))
        self.assertFalse(DiffDataFiles.should_key_be_ignored(lines, ''))