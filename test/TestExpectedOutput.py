fileOld = "test-old-file.txt"
fileNew = "test-new-file.txt"
fileOutput = "actual-output-do-not-commit.txt"

import DiffDataFiles

DiffDataFiles.diffDataFiles(fileOld, fileNew, fileOutput, ["IgnoreMe"])