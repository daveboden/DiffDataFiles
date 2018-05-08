fileOld = "ignore-no-columns/test-case-ignore-no-columns-old.txt"
fileNew = "ignore-no-columns/test-case-ignore-no-columns-new.txt"
fileOutput = "output/actual-ignore-no-columns-output-do-not-commit.txt"
fileExpected = "ignore-no-columns/test-case-ignore-no-columns-expected-output.txt"

import DiffDataFiles
import filecmp

DiffDataFiles.diff_data_files(
    file_old = fileOld,
    file_new = fileNew,
    file_output = fileOutput,
    ignore_blank_to_no_columns = ["IgnoreBlankToNo"]
)

assert filecmp.cmp(fileExpected, fileOutput)