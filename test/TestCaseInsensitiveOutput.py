fileOld = "case-insensitive/test-case-insensitive-old.txt"
fileNew = "case-insensitive/test-case-insensitive-new.txt"
fileOutput = "output/actual-case-insensitive-output-do-not-commit.txt"
fileExpected = "case-insensitive/test-case-insensitive-expected-output.txt"

import DiffDataFiles
import filecmp

DiffDataFiles.diff_data_files(
    file_old = fileOld,
    file_new = fileNew,
    file_output = fileOutput,
    ignore_case_columns= ["CaseInsensitive"]
)

assert filecmp.cmp(fileExpected, fileOutput)