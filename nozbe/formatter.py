import datetime

DATE_FORMAT = "%Y-%m-%d"
DUE_DATE_FORMAT = "%B %-d"
TASK_OUTPUT_FORMAT = ". {}  #{}"


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
