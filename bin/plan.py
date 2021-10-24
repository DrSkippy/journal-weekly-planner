from planner import model
from planner.columns import columns

def day_input(s,d):
    a = input("{} ({}): ".format(s,d))
    if a == "":
        tmp = d.strip("[]")
        if tmp != "":
            # use the default
            return tmp.lower().split(",")
        else:
            return None
    days = a.strip().lower().split(" ")
    return days


if "__main__" == __name__:
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
        doc1 = w.plan_paper_week_days()
        output_file.write(columns(doc1, 1))

    with open("./plan.nozbe", "w") as output_file:
        doc2 = w.plan_nozbe()
        output_file.write(columns(doc2, 1))
