fileOld = "test-old-file.txt"
fileNew = "test-new-file.txt"
fileOutput = "output/actual-output-do-not-commit.txt"
fileExpected = "test-expected-output-file.txt"

import DiffDataFiles
import filecmp

DiffDataFiles.diff_data_files(
    file_old = fileOld,
    file_new = fileNew,
    file_output = fileOutput,
    ignore_columns = ["IgnoreMe"],
    ignore_keys = ["G-DIFFERENT_ButIgnoreKey"]
)

assert filecmp.cmp(fileExpected, fileOutput)