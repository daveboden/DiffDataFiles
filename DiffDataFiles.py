#!/usr/bin/env python
import csv
import bisect


def diff_data_files(file_old, file_new, file_output, ignore_columns=None,
                    ignore_keys=None, max_count=None, key_column_count=1,
                    ignore_case_columns=None,column_names=None,ignore_blank_to_no_columns=None):

    no_values = ['N', 'No', 'no', 'None']

    csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)

    count = 0
    difference_columns = {}

    difference_count = [0]
    extra_count = [0]
    missing_count = [0]

    #Closure which has access to the column configurations. Data must be passed in.
    def diff_exists(data_old, data_new, fieldname):
        if ignore_blank_to_no_columns and fieldname in ignore_blank_to_no_columns and data_old[fieldname] == "" and data_new[fieldname] in no_values:
            return False

        if ignore_case_columns and fieldname in ignore_case_columns:
            return data_old[fieldname].lower() != data_new[fieldname].lower()
        else:
            return data_old[fieldname] != data_new[fieldname]

    with open(file_old, "rb") as csvfileOld:
        with open(file_new, "rb") as csvfileNew:

            reader_old = csv.DictReader(csvfileOld, dialect='piper', fieldnames=column_names)
            reader_new = csv.DictReader(csvfileNew, dialect='piper', fieldnames=column_names)

            key_columns = reader_new.fieldnames[:key_column_count]
            fieldnames = reader_new.fieldnames[key_column_count:]  # Remove key column

            # Will throw StopIterator exceptions if the files are unexpectedly empty
            data_old = reader_old.next()
            data_new = reader_new.next()

            with open(file_output, "wb") as reportFile:
                writer_report = csv.writer(reportFile, dialect='piper')

                header_row = list(key_columns)
                for fieldname in fieldnames:
                    header_row.append(fieldname + ' Old')
                    header_row.append(fieldname + ' New')
                    header_row.append(fieldname + ' Equiv')
                writer_report.writerow(header_row)

                def print_extra(new_row):
                    if not should_key_be_ignored(ignore_keys, new_row[key_columns[0]]):
                        extra_count[0] += 1
                        output_r = list(map(lambda x: new_row[x], key_columns))
                        for f in fieldnames:
                            output_r.append("")
                            output_r.append(new_row[f])
                            output_r.append("extra")
                        writer_report.writerow(output_r)

                def print_missing(old_row):
                    if not should_key_be_ignored(ignore_keys, old_row[key_columns[0]]):
                        missing_count[0] += 1
                        output_r = list(map(lambda x: old_row[x], key_columns))
                        for f in fieldnames:
                            output_r.append(old_row[f])
                            output_r.append("")
                            output_r.append("missing")
                        writer_report.writerow(output_r)

                while True:
                    # Now that we have the first row of both files, let's compare them then iterate.
                    count += 1
                    if max_count and count > max_count:
                        break

                    if less_than(data_old, data_new, key_columns):
                        print_missing(data_old)
                        try:
                            data_old = reader_old.next()
                        except StopIteration:
                            # No more old rows. Empty remaining new rows and stop iterating
                            print_extra(data_new)
                            for data_new_rest in reader_new:
                                print_extra(data_new_rest)
                            break

                    elif greater_than(data_old, data_new, key_columns):
                        print_extra(data_new)
                        try:
                            data_new = reader_new.next()
                        except StopIteration:
                            # No more new rows. Empty remaining old rows and stop iterating
                            print_missing(data_old)
                            for dataOldRest in reader_old:
                                print_extra(dataOldRest)
                            break

                    else:
                        if not should_key_be_ignored(ignore_keys, data_new[key_columns[0]]):
                            # Compare and only print if there are differences
                            differences = False
                            output_row = list(map(lambda x: data_new[x], key_columns))
                            for fieldname in fieldnames:
                                output_row.append(data_old[fieldname])
                                output_row.append(data_new[fieldname])

                                if diff_exists(data_old, data_new, fieldname):
                                    output_row.append("no")
                                    if not ignore_columns or fieldname not in ignore_columns:
                                        differences = True

                                        if fieldname in difference_columns:
                                            difference_columns[fieldname] += 1
                                        else:
                                            difference_columns[fieldname] = 1
                                else:
                                    output_row.append("yes")

                            if differences:
                                difference_count[0] += 1
                                writer_report.writerow(output_row)

                        # Read in another old row and another new row.
                        try:
                            data_old = reader_old.next()
                        except StopIteration:
                            # No more old rows. Empty remaining new rows and stop iterating
                            for data_new_rest in reader_new:
                                print_extra(data_new_rest)
                            break

                        try:
                            data_new = reader_new.next()
                        except StopIteration:
                            # No more new rows. Empty remaining old rows and stop iterating
                            for dataOldRest in reader_old:
                                print_extra(dataOldRest)
                            break

    print "Different rows count =", difference_count[0]
    print "Missing rows count =", missing_count[0]
    print "Extra rows count =", extra_count[0]

    sorted_difference_count = sorted(difference_columns.items(), key=lambda k: (-k[1], k[0]))
    if len(sorted_difference_count) > 0:
        print "-- Column diffs --"
    for sdc in sorted_difference_count:
        print sdc[0] + ": " + str(sdc[1])


def read_keys_file_into_array(filename):
    with open(filename, "r") as f_in:
        lines = (line.rstrip() for line in f_in)  # All lines including the blank ones
        lines = (line for line in lines if line)  # Non-blank lines
        return list(lines)


def should_key_be_ignored(ignore_keys, key_to_check):
    if not ignore_keys:
        return False
    else:
        'Locate the leftmost value exactly equal to x'
        i = bisect.bisect_left(ignore_keys, key_to_check)
        return i != len(ignore_keys) and ignore_keys[i] == key_to_check


def less_than(data_old, data_new, key_cols):
    for key_column in key_cols:
        if data_old[key_column] < data_new[key_column]:
            return True
        elif data_old[key_column] > data_new[key_column]:
            return False
    return False


def greater_than(data_old, data_new, key_cols):
    for key_column in key_cols:
        if data_old[key_column] > data_new[key_column]:
            return True
        elif data_old[key_column] < data_new[key_column]:
            return False
    return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Diff pipe separate data files that are already sorted by key in the first column.'
    )
    parser.add_argument("--old_file", required=True)
    parser.add_argument("--new_file", required=True)
    parser.add_argument("--output_file", required=True)
    parser.add_argument("--ignore_keys_file")
    parser.add_argument("--ignore_columns")
    parser.add_argument("--max_count", type=int)
    parser.add_argument("--key_column_count", type=int)
    parser.add_argument("--column_names")
    parser.add_argument("--ignore_blank_to_no_columns")
    args = parser.parse_args()

    if args.ignore_keys_file:
        ignore_keys_main = read_keys_file_into_array(args.ignore_keys_file)
    else:
        ignore_keys_main = None

    if args.ignore_columns:
        ignore_columns_main = args.ignore_columns.split(',')
    else:
        ignore_columns_main = None

    if args.column_names:
        column_names_main = args.column_names.split(',')
    else:
        column_names_main = None

    if args.ignore_blank_to_no_columns:
        ignore_blank_to_no_columns_main = args.ignore_blank_to_no_columns.split(',')
    else:
        ignore_blank_to_no_columns_main = None

    diff_data_files(args.old_file,
                    args.new_file,
                    args.output_file,
                    ignore_keys=ignore_keys_main,
                    ignore_columns=ignore_columns_main,
                    key_column_count=args.key_column_count,
                    column_names=column_names_main,
                    ignore_blank_to_no_columns=ignore_blank_to_no_columns_main)
