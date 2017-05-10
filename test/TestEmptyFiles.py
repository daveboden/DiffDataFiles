import unittest
import DiffDataFiles

fileOld = "test-old-file.txt"
fileNew = "test-new-file.txt"
fileEmpty = "test-empty-file.txt"
fileHeadersOnly = "test-headersonly-file.txt"
fileOutput = "output-not-expected.txt"

class TestStringMethods(unittest.TestCase):

    def test_new_empty(self):
        with self.assertRaises(TypeError):
            DiffDataFiles.diff_data_files(fileOld, fileEmpty, fileOutput, ["IgnoreMe"])

    def test_old_empty(self):
        with self.assertRaises(StopIteration):
            DiffDataFiles.diff_data_files(fileEmpty, fileNew, fileOutput, ["IgnoreMe"])

    def test_both_empty(self):
        with self.assertRaises(TypeError):
            DiffDataFiles.diff_data_files(fileEmpty, fileEmpty, fileOutput, ["IgnoreMe"])

    def test_new_headers_only(self):
        with self.assertRaises(StopIteration):
            DiffDataFiles.diff_data_files(fileOld, fileHeadersOnly, fileOutput, ["IgnoreMe"])

    def test_old_headers_only(self):
        with self.assertRaises(StopIteration):
            DiffDataFiles.diff_data_files(fileHeadersOnly, fileNew, fileOutput, ["IgnoreMe"])

    def test_both_headers_only(self):
        with self.assertRaises(StopIteration):
            DiffDataFiles.diff_data_files(fileHeadersOnly, fileHeadersOnly, fileOutput, ["IgnoreMe"])