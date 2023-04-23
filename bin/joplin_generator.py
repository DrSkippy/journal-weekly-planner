#!/usr/bin/env python3
import argparse
import csv
import re
import sys

import requests

from nozbe.formatter import *
from joplin.task_import import *

USE_DESCRIPTION = """
Harvest tasks from joplin notebook @nozbe and create Nozbe tasks
"""

def parse_agrs():
    parser = argparse.ArgumentParser(description=USE_DESCRIPTION)
    parser.add_argument('-s', '--stride', default=0,
                        help='Float, measured in days, fraction of day makes more than one task per day')
    parser.add_argument('-w', '--weekdays', action='store_true', default=False,
                        help='If tasks fall on weekends, skip to next Monday')
    parser.add_argument('-d', '--due_date', default=None,
                        help='Set due date instead of reading from Joplin')
    parser.add_argument('hash', nargs='*', default=None,
                        help='Common hash tag for all tasks')
    parser.add_argument('-f', '--final', default=False, action='store_true', help='Updates Joplin notes')
    return parser.parse_args()



def parse_input(final=False):
    task_dicts = get_notes_tasks_list()
    for task in task_dicts:
        comments = [f'Generated {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}']
        comments.append(task['comments'])
        fields = [task["title"], task['due_date']]
        fields.extend(task['hash_tags'])
        yield fields, comments
    if final:
        for task in task_dicts:
            update_notes([task["note_id"]])



if __name__ == "__main__":
    args = parse_agrs()

    date_stride = datetime.timedelta(days=float(args.stride))

    line_parser = parse_input(args.final)
    due_date = None
    for fields, comments in line_parser:
        date_str = fields[1] if args.due_date is None else args.due_date
        due_date, due_date_str = calculate_due_date(due_date, date_str, date_stride, args.weekdays)
        if args.hash is not None:
            fields.extend(args.hash)
        task_lines = format_output(fields, comments, due_date_str)
        print("\n".join(task_lines))
