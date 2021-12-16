#!/usr/bin/env python3
import argparse
import csv
import datetime
import sys

example = """
Do this, 2021-12-16, [task comment: mom says you should do this]
Do that, 2021-12-18, Every Week
I'm mister Burns, 2022-02-01, Every Weekday, Inbox
"Blah, blah, blah", 2022-03-01, Every Week, Aspen Mesh, 6 h 
# a comment line
"""

doc = """
Make a file with tasks:
"text", due_date, hash0, hash2, ..., [comment1], [comment2], ...
...
# comment line
<eof>

Example lines:

{}

Cut and paste lines and then update with something like this to set task parameters.
    1,$s/$/,2022-05-01, Movies, 2 h, Home Computer
""".format(example)

FMT = "%Y-%m-%d"
DDFMT = "%B %-d"

parser = argparse.ArgumentParser(description=doc)
parser.add_argument('-s', '--stride', default=0,
                    help='Float, measured in days, fraction of day makes more than one task per day')
parser.add_argument('-w', '--weekdays', action='store_true', default=False,
                    help='If tasks fall on weekends, skip to next Monday')
parser.add_argument('-d', '--due_date', default=None, help='Set due date instead of reading from file')
parser.add_argument('hash', nargs='*', default=None, help='Common hash tag for all tasks')
parser.add_argument('-f', '--file', action='store_true', default=False, help='Generate an example file')
args = parser.parse_args()

if args.file:
    print(example)
    sys.exit(0)

date_stride = datetime.timedelta(days=float(args.stride))

rdr = csv.reader(sys.stdin)
i = 0  # tasks created
for raw_row in rdr:
    raw_row = [x.strip(" ") for x in raw_row]
    if len(raw_row) == 0 or raw_row[0].startswith("#"):
        # input comment lines
        continue
    else:
        i += 1

    row, comment = [], []
    for field in raw_row:
        if field.startswith("["):
            # this is a nozbe comment
            # you can have as many as you want
            comment.append(field.strip("[]"))
        else:
            row.append(field)

    if args.due_date is not None:
        _dt = args.due_date
    else:
        _dt = row[1]
    dat_str = datetime.datetime.strptime(_dt, FMT).date() + (i - 1) * date_stride
    if args.weekdays:
        while dat_str.weekday() > 4:
            # exclude weekends
            i += 1
            dat_str = datetime.datetime.strptime(_dt, FMT).date() + (i - 1) * date_stride

    if args.hash is not None:
        row.extend(args.hash)

    out_formatter = ". {}  #{}"
    for _ in range(len(row) - 2):
        out_formatter += "  #{}"

    print(out_formatter.format(row[0], dat_str.strftime(DDFMT), *row[2:]))
    if len(comment) > 0:
        print("\n".join(comment))
