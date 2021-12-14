#!/usr/bin/env python3
documentation = """
Example lines:

Do this, 2021-12-16
Do that, 2021-12-18, Every Week
I'm mister Burns, 2022-02-01, Every Weekday, Inbox
"Blah, blah, blah", 2022-03-01, Every Week, Aspen Mesh, 6 h 


So cut and paste lines and then update with something like this to set task parameters.
    1,$s/$/,2022-05-01, Movies, 2 h, Home Computer
"""
import csv
import sys
import datetime 

FMT = "%Y-%m-%d"
DDFMT = "%B %-d"

date_stride = datetime.timedelta(days=0.25)

rdr = csv.reader(sys.stdin)
i = 0
for rawrow in rdr:
    rawrow = [x.strip(" ") for x in rawrow]
    if rawrow[0].startswith("#"):
        # comment lines
        continue
    else:
        i += 1
    row = []
    comment = []
    for field in rawrow:
        if field.startswith("["):
            # this is a nozbe comment
            comment.append(field.strip("[]"))
        else:
            row.append(field)
    # text due_date hash1 hash2 ...
    dat_str = datetime.datetime.strptime(row[1], FMT).date() + (i-1) * date_stride
    while dat_str.weekday() > 4:
        # exclude weekends
        i += 1 
        dat_str = datetime.datetime.strptime(row[1], FMT).date() + (i-1) * date_stride
    out_formatter = ". {}  #{}"
    for _ in range(len(row)-2):
        out_formatter += "  #{}"
    print(out_formatter.format(row[0], dat_str.strftime(DDFMT), *row[2:]))
    if len(comment) > 0:
        print("\n".join(comment))
