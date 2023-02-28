#!/usr/bin/env python3
import argparse
import csv
import datetime
import sys
import re
import requests

EXAMPLE_FILE = """
# a comment line
(Alembic) test old file on old hologram apparatus, 2021-12-01, Projects, [The first task in the file.]
"(Alembic) bonus, sound track for pendulums?", 2021-12-01, Projects, [Amazing task!]
(Alembic) packing list/BOM for alembic, 2021-12-01, Projects
(Alembic) communicate with kevin re progress and ideas, 2021-12-01, Projects
(Alembic) sketch notes of the arch of holographic universe discussion, 2021-12-01, Projects
(Alembic) reread and update notes, 2021-12-01, Projects
(Alembic) check batteries for lasers, 2021-12-01, Projects
(Alembic) check batteries for lights (even as backup), 2021-12-01, Projects
"""

USE_DESCRIPTION = """
Make a file with tasks:
"text", due_date, hash0, hash2, ..., [comment1], [comment2], ...
"""

DATE_FORMAT = "%Y-%m-%d"
DUE_DATE_FORMAT = "%B %-d"
TASK_OUTPUT_FORMAT = ". {}  #{}"

lre = re.compile('https://substack.com/redirect/.*?[?]')


def parse_agrs():
    parser = argparse.ArgumentParser(description=USE_DESCRIPTION)
    parser.add_argument('-s', '--stride', default=0,
                        help='Float, measured in days, fraction of day makes more than one task per day')
    parser.add_argument('-w', '--weekdays', action='store_true', default=False,
                        help='If tasks fall on weekends, skip to next Monday')
    parser.add_argument('-d', '--due_date', default=None,
                        help='Set due date instead of reading from file')
    parser.add_argument('hash', nargs='*', default=None,
                        help='Common hash tag for all tasks')
    parser.add_argument('-f', '--file', action='store_true', default=False,
                        help='Generate an example file')
    parser.add_argument('-e', '--extract-data-machina', default=None,
                        help='Read in data machina email export file')
    return parser.parse_args()


def fetch_links(in_file_name):
    document_data = []
    with open(in_file_name, "r") as infile:
        for row in infile:
            document_data.append(row.strip(' \n\r='))
    document = ''.join(document_data)
    links = set([x[:-1].replace("%", "=") for x in lre.findall(document) if len(x) < 100])
    return links


def parse_data_machina(in_file_name):
    links = fetch_links(in_file_name)
    for url in links:
        try:
            resp = requests.get(url)
            try:
                u, _ = resp.url.split("?")
            except ValueError:
                u = resp.url
            if "substack" not in u:
                fields = ["(DataMachina) Visit link", "2020-01-01", "Continuing Education"]
                comments = [f'Generated {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
                            f"Source: {in_file_name}",
                            f"Total links this email: {len(links)}",
                            f"Visit: {u}"]
                yield fields, comments
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidSchema) as e:
            continue


def parse_input():
    rdr = csv.reader(sys.stdin)
    for row in rdr:
        if not row or row[0].startswith("#"):
            continue
        comments, fields = [f'Generated {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}'], []
        for field in row:
            if field.strip().startswith("["):
                # this is a Nozbe comment
                comments.append(field.strip(" []"))
            else:
                fields.append(field.strip())
        yield fields, comments


def calculate_due_date(due_date, date_str, date_stride, weekdays_only):
    if date_stride == datetime.timedelta(days=0) or due_date is None:
        due_date = datetime.datetime.strptime(date_str, DATE_FORMAT).date()
    else:
        due_date += date_stride
    while weekdays_only and due_date.weekday() > 4:
        due_date += date_stride
    return due_date, due_date.strftime(DUE_DATE_FORMAT)


def format_output(fields, comments, date_str):
    task_lines = []
    output_formatter = "".join([TASK_OUTPUT_FORMAT] + [" #{}"] * (len(fields) - 2))
    task_lines.append(output_formatter.format(fields[0], date_str, *fields[2:]))
    if len(comments) > 0:
        task_lines.extend(comments)
    return task_lines


if __name__ == "__main__":
    args = parse_agrs()
    if args.file:
        print(EXAMPLE_FILE)
        sys.exit(0)

    date_stride = datetime.timedelta(days=float(args.stride))

    if args.extract_data_machina is None:
        line_parser = parse_input()
    else:
        line_parser = parse_data_machina(args.extract_data_machina)

    due_date = None
    for fields, comments in line_parser:
        date_str = fields[1] if args.due_date is None else args.due_date
        due_date, due_date_str = calculate_due_date(due_date, date_str, date_stride, args.weekdays)
        if args.hash is not None:
            fields.extend(args.hash)
        task_lines = format_output(fields, comments, due_date_str)
        print("\n".join(task_lines))
