import datetime

from planner import model
from planner.columns import columns


def day_input(s, valid_days_list = ["su", "m", "t", "w", "h", "f", "sa"]):
    valid_days = False
    while not valid_days:
        a = input("{:15} ({} {}) ({}): ".format(s[0], s[2], s[3], s[4].strip("[]").replace(",", " ")))
        update_weekly_time = s[2]  # default time unless changed
        a = a.strip()
        if a == "":
            updated_days = s[4].strip("[]").lower().split(",") if s[4] != "" else []
            valid_days = True
        else:
            tmp_list = a.strip().lower().split(" ")
            try:
                # if the last token is a number, it is the weekly time
                update_weekly_time = str(float(tmp_list[-1]))
                tmp_list = tmp_list[:-1] # remove the last token
            except ValueError:
                # use the default
                pass
            if len(tmp_list) == 0 or tmp_list[0].startswith("x"):
                updated_days = []
                valid_days = True
            elif all([x in valid_days_list for x in tmp_list]):
                updated_days = tmp_list
                valid_days = True
            else:
                print("Invalid day or days. Please re-enter...")
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
        days, weekly_time = day_input(activity, valid_days_list = list(w.days_of_week.keys()))
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
