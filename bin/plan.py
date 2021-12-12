import datetime

from planner import model
from planner.columns import columns

def day_input(s,d):
    a = input("{} ({}): ".format(s,d))
    days = None
    if a == "":
        tmp = d.strip("[]")
        if tmp != "":
            # use the default
            days = tmp.lower().split(",")
    else:
        tmp = a.strip().lower().split(" ")
        if len(tmp) > 0 and not tmp[0].startswith("x"):
            days = tmp
    return days


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

    for activity in m.data:
        activity_name = activity[0]
        default_days = activity[4]
        days = day_input(activity_name, default_days)
        if days is not None:
            w.add_activity(activity, days)

    print()
    doc = w.plan_paper()
    print(columns(doc))

    with open("./plan.html", "w") as output_file:
        doc1 = w.plan_paper_week_days(date_obj)
        output_file.write(columns(doc1, 1))

    with open("./plan.nozbe", "w") as output_file:
        doc2 = w.plan_nozbe(date_obj)
        output_file.write(columns(doc2, 1))
