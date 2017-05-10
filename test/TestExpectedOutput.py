fileOld = "test-old-file.txt"
fileNew = "test-new-file.txt"
fileOutput = "output/actual-output-do-not-commit.txt"

import DiffDataFiles

DiffDataFiles.diff_data_files(fileOld, fileNew, fileOutput, ["IgnoreMe"], ["G-DIFFERENT_ButIgnoreKey"])