#!/usr/bin/env python
import csv
import bisect


def diffDataFiles(fileOld, fileNew, fileOutput, ignoreColumns=None, ignoreKeys=None, maxCount=None):

    csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)

    count=0
    differenceColumns = {}

    differenceCount = [0]
    extraCount = [0]
    missingCount = [0]

    with open(fileOld, "rb") as csvfileOld:
        with open(fileNew, "rb") as csvfileNew:

            readerOld = csv.DictReader(csvfileOld, dialect='piper')
            readerNew = csv.DictReader(csvfileNew, dialect='piper')

            keyColumn = readerNew.fieldnames[0]
            fieldnames = readerNew.fieldnames[1:] #Remove key column

            #Will throw StopIterator exceptions if the files are unexpectedly empty
            dataOld = readerOld.next()
            dataNew = readerNew.next()

            with open(fileOutput, "wb") as reportFile:
                writerReport = csv.writer(reportFile, dialect='piper')

                headerRow = [keyColumn]
                for fieldname in fieldnames:
                    headerRow.append(fieldname + ' Old')
                    headerRow.append(fieldname + ' New')
                    headerRow.append(fieldname + ' Equiv')
                writerReport.writerow(headerRow)

                def printExtra(newRow):
                    if not shouldKeyBeIgnored(ignoreKeys, newRow[keyColumn]):
                        extraCount[0] += 1
                        outputRow = [newRow[keyColumn]]
                        for fieldname in fieldnames:
                            outputRow.append("")
                            outputRow.append(newRow[fieldname])
                            outputRow.append("extra")
                        writerReport.writerow(outputRow)

                def printMissing(oldRow):
                    if not shouldKeyBeIgnored(ignoreKeys, oldRow[keyColumn]):
                        missingCount[0] += 1
                        outputRow = [oldRow[keyColumn]]
                        for fieldname in fieldnames:
                            outputRow.append(oldRow[fieldname])
                            outputRow.append("")
                            outputRow.append("missing")
                        writerReport.writerow(outputRow)

                while True:
                    #Now that we have the first row of both files, let's compare them then iterate.
                    count += 1
                    if maxCount != None and count > maxCount:
                        break

                    if dataOld[keyColumn] < dataNew[keyColumn]:
                        printMissing(dataOld)
                        try:
                            dataOld = readerOld.next()
                        except StopIteration:
                            #No more old rows. Empty remaining new rows and stop iterating
                            printExtra(dataNew)
                            for dataNewRest in readerNew:
                                printExtra(dataNewRest)
                            break

                    elif dataOld[keyColumn] > dataNew[keyColumn]:
                        printExtra(dataNew)
                        try:
                            dataNew = readerNew.next()
                        except StopIteration:
                            #No more new rows. Empty remaining old rows and stop iterating
                            printMissing(dataOld)
                            for dataOldRest in readerOld:
                                printExtra(dataOldRest)
                            break

                    else:
                        if not shouldKeyBeIgnored(ignoreKeys, dataNew[keyColumn]):
                            #Compare and only print if there are differences
                            differences = False
                            outputRow = [dataNew[keyColumn]]
                            for fieldname in fieldnames:
                                outputRow.append(dataOld[fieldname])
                                outputRow.append(dataNew[fieldname])
                                if dataOld[fieldname] != dataNew[fieldname]:
                                    outputRow.append("N")
                                    if ignoreColumns == None or fieldname not in ignoreColumns:
                                        differences = True

                                        if differenceColumns.has_key(fieldname):
                                            differenceColumns[fieldname] += 1
                                        else:
                                            differenceColumns[fieldname] = 1
                                else:
                                    outputRow.append("Y")

                            if differences:
                                differenceCount[0] += 1
                                writerReport.writerow(outputRow)

                        #Read in another old row and another new row.
                        try:
                            dataOld = readerOld.next()
                        except StopIteration:
                            #No more old rows. Empty remaining new rows and stop iterating
                            for dataNewRest in readerNew:
                                printExtra(dataNewRest)
                            break

                        try:
                            dataNew = readerNew.next()
                        except StopIteration:
                            #No more new rows. Empty remaining old rows and stop iterating
                            for dataOldRest in readerOld:
                                printExtra(dataOldRest)
                            break

    print "Different rows count =", differenceCount[0]
    print "Missing rows count =", missingCount[0]
    print "Extra rows count =", extraCount[0]

    sortedDifferenceCount = sorted(differenceColumns.items(), key=lambda k: (-k[1],k[0]))
    if len(sortedDifferenceCount) > 0:
        print "-- Column diffs --"
    for sdc in sortedDifferenceCount:
        print sdc[0] + ": " + str(sdc[1])

def readKeysFileIntoArray(filename):
    with open(filename, "r") as f_in:
        lines = (line.rstrip() for line in f_in)  # All lines including the blank ones
        lines = (line for line in lines if line)  # Non-blank lines
        return list(lines)

def shouldKeyBeIgnored(ignoreKeys, keyToCheck):
    if ignoreKeys == None:
        return False
    else:
        'Locate the leftmost value exactly equal to x'
        i = bisect.bisect_left(ignoreKeys, keyToCheck)
        return i != len(ignoreKeys) and ignoreKeys[i] == keyToCheck

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Diff pipe separate data files that are already sorted by key in the first column.')
    parser.add_argument("--oldFile", required=True)
    parser.add_argument("--newFile", required=True)
    parser.add_argument("--outputFile", required=True)
    parser.add_argument("--ignoreKeysFile")
    parser.add_argument("--ignoreColumns")
    parser.add_argument("--maxCount", type=int)
    args = parser.parse_args()

    if(args.ignoreKeysFile != None):
        ignoreKeys = readKeysFileIntoArray(args.ignoreKeysFile)
    else:
        ignoreKeys = None

    diffDataFiles(args.oldFile,
                  args.newFile,
                  args.outputFile,
                  ignoreKeys=ignoreKeys,
                  ignoreColumns=args.ignoreColumns.split(','))
