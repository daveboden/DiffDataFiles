fileOld = "test-old-two-key-file.txt"
fileNew = "test-new-two-key-file.txt"
fileOutput = "output/actual-output-two-key-do-not-commit.txt"

import DiffDataFiles

DiffDataFiles.diff_data_files(file_old=fileOld,
                              file_new=fileNew,
                              file_output=fileOutput,
                              key_column_count=2)