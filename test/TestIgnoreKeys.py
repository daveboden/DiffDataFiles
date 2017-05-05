import unittest
import DiffDataFiles

filename = "ignore-keys-test-file.txt"

class TestStringMethods(unittest.TestCase):

    def test_read(self):
        lines = DiffDataFiles.readKeysFileIntoArray(filename)
        self.assertEqual(['AAA', 'BBB', 'CCC'], lines)
        print lines
        self.assertTrue(DiffDataFiles.shouldKeyBeIgnored(lines, "AAA"))
        self.assertFalse(DiffDataFiles.shouldKeyBeIgnored(lines, "JJJ"))
        self.assertFalse(DiffDataFiles.shouldKeyBeIgnored(lines, ''))