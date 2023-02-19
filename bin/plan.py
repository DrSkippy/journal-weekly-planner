import datetime

from planner import model
from planner.columns import columns


def day_input(s):
    a = input("{:15} ({} {}) ({}): ".format(s[0],
                                            s[2],
                                            s[3],
                                            s[4].strip("[]").replace(",", " ")))
    updated_days = None
    update_weekly_time = s[2]
    if a == "":
        tmp = s[4].strip("[]")
        if tmp != "":
            # use the default
            updated_days = tmp.lower().split(",")
    else:
        tmp = a.strip().lower().split(" ")
        try:
            update_weekly_time = str(float(tmp[-1]))
            tmp = tmp[:-1]
        except ValueError:
            update_weekly_time = s[2]
        if len(tmp) > 0 and not tmp[0].startswith("x"):
            updated_days = tmp
    return updated_days, update_weekly_time


if "__main__" == __name__:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--sunday-start-date', dest='start_date', type=str,
                        default=None, help='sunday Start date')
    args = parser.parse_args()

    if args.start_date is None:
        date_obj = args.start_date
    else:
        date_obj = datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()

    m = model.Activities()
    print(m)
    w = model.Week()

    print("x - no days; enter number at the end to update time")
    for activity in m.data:
        days, weekly_time = day_input(activity)
        if days is not None:
            w.add_activity(activity, days, weekly_time)

    print()
    doc = w.plan_paper()
    print(columns(doc))

    with open("./plan.txt", "w") as output_file:
        output_file.write(columns(doc, 2))
        output_file.write("\n")

    with open("./plan.html", "w") as output_file:
        doc1 = w.plan_paper_week_days(date_obj)
        output_file.write(columns(doc1, 1))

    with open("./plan.nozbe", "w") as output_file:
        doc2 = w.plan_nozbe(date_obj)
        output_file.write(columns(doc2, 1))
