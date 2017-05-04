import csv

def diffDataFiles(fileOld, fileNew, fileOutput, ignoreColumns, maxCount = None):

    csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)

    count=0
    differenceCount = {}

    with open(fileOld, "rb") as csvfileOld, open(fileNew, "rb") as csvfileNew, open(fileOutput, "wb") as reportFile:

        writerReport = csv.writer(reportFile, dialect='piper')
        readerOld = csv.DictReader(csvfileOld, dialect='piper')
        readerNew = csv.DictReader(csvfileNew, dialect='piper')

        keyColumn = readerNew.fieldnames[0]
        fieldnames = readerNew.fieldnames[1:] #Remove key column

        def printExtra(newRow):
            outputRow = [newRow[keyColumn]]
            for fieldname in fieldnames:
                outputRow.append("")
                outputRow.append(newRow[fieldname])
                outputRow.append("extra")
            writerReport.writerow(outputRow)

        def printMissing(oldRow):
            outputRow = [oldRow[keyColumn]]
            for fieldname in fieldnames:
                outputRow.append(oldRow[fieldname])
                outputRow.append("")
                outputRow.append("missing")
            writerReport.writerow(outputRow)

        #Will throw StopIterator exceptions if the files are unexpectedly empty
        dataOld = readerOld.next()
        dataNew = readerNew.next()

        headerRow = [keyColumn]
        for fieldname in fieldnames:
            headerRow.append(fieldname + ' Old')
            headerRow.append(fieldname + ' New')
            headerRow.append(fieldname + ' Equiv')
        writerReport.writerow(headerRow)

        while True:
            #Now that we have the first row of both files, let's compare them then iterate.
            count = count + 1
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
                #Compare and only print if there are differences
                differences = False
                outputRow = [dataNew[keyColumn]]
                for fieldname in fieldnames:
                    outputRow.append(dataOld[fieldname])
                    outputRow.append(dataNew[fieldname])
                    if dataOld[fieldname] != dataNew[fieldname]:
                        outputRow.append("N")
                        if fieldname not in ignoreColumns:
                            differences = True

                            if differenceCount.has_key(fieldname):
                                differenceCount[fieldname] = differenceCount[fieldname] + 1
                            else:
                                differenceCount[fieldname] = 1
                    else:
                        outputRow.append("Y")

                if differences:
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

    print differenceCount