import csv
import datetime


class Activities:
    data = []
    header = []
    file_path = "./config/master.csv"

    def __init__(self):
        with open(self.file_path, "r") as input_file:
            rdr = csv.reader(input_file)
            first = True
            for row in rdr:
                if first:
                    self.header = row
                    first = False
                else:
                    self.data.append(row)

    def get_activity(self, activity_name):
        for x in self.data:
            if x[0] == activity_name:
                return x

    def __str__(self):
        res = [" - ".join(self.header), "=" * 30]
        for x in self.data:
            res.append(" - ".join(x))
        return "\n".join(res) + "\n"


class Week:
    UNITS_HOUR = "hour"

    ACTIVITY_NAME = 0
    ACTIVITY_TIME = 2
    ACTIVITY_UNITS = 3

    DAYS_ACTIVITY = 0
    DAYS_DAILY_TIME = 1
    DAYS_UNITS = 2

    days_of_week = {
        "su": "Sunday",
        "m": "Monday",
        "t": "Tuesday",
        "w": "Wednesday",
        "h": "Thursday",
        "f": "Friday",
        "sa": "Saturday"
    }
    days = {
        x: [] for x in days_of_week  # (activity, hours/day OR cnt/day, unit)
    }
    activity_list = set()

    def add_activity(self, activity, days):
        self.activity_list.add(activity[0])
        if len(days) > 0 and days[0] == "a":
            # all days of week
            days = list(self.days_of_week.keys())
        n = len(days)
        for d in days:
            if activity[3] == self.UNITS_HOUR:
                self.days[d].append((activity[self.ACTIVITY_NAME],
                                     round(float(activity[self.ACTIVITY_TIME]) / n, 2),
                                     activity[self.ACTIVITY_UNITS]))
            else:
                self.days[d].append((activity[self.ACTIVITY_NAME],
                                     round(float(activity[self.ACTIVITY_TIME]), 2),
                                     activity[self.ACTIVITY_UNITS]))

    def plan_paper(self):
        res = ["<hr>"]
        for d in self.days:
            res.append(self.days_of_week[d])
            res.append("<hr>")
            for x in self.days[d]:
                if x[self.DAYS_UNITS] == self.UNITS_HOUR:
                    res.append("{:13} ({:4d} min): __________".format(x[self.DAYS_ACTIVITY],
                                                                      int(x[self.DAYS_DAILY_TIME] * 60)))
                else:  # count
                    res.append(
                        "{:13} ({:4d} {}): __________".format(x[self.DAYS_ACTIVITY],
                                                              int(x[self.DAYS_DAILY_TIME]),
                                                              x[self.DAYS_UNITS]))
            res.append("<hr>")
        return res

    def plan_paper_week_days(self):
        res = ["<pre>\n"]
        res.append("<hr>")
        fmt = "{:13}" + "| {:16}" * 7
        res.append(fmt.format(*tuple(["Activity"] + [self.days_of_week[i] for i in self.days_of_week])))
        res.append("<hr>")
        for activity in self.activity_list:
            row = ["{:13}".format(activity)]
            for d in self.days:
                for x in self.days[d]:
                    if x[self.DAYS_ACTIVITY] == activity:
                        if x[self.DAYS_UNITS] == self.UNITS_HOUR:
                            row.append("{:4d} min: ______ ".format(int(x[self.DAYS_DAILY_TIME] * 60)))
                        else:  # count
                            row.append("{:4d} {}: ______ ".format(int(x[self.DAYS_DAILY_TIME]),
                                                                  x[self.DAYS_UNITS]))
                        break
                else:
                    row.append(" " * 17)
            res.append("|".join(row))
        res.append("<hr>")
        res.append("</pre>\n")
        return res

    def plan_nozbe(self):
        res = []
        for d in self.days:
            for x in self.days[d]:
                res.append(
                    ". {} for {} {} #{} #{}".format(x[self.DAYS_ACTIVITY],
                                                    x[self.DAYS_DAILY_TIME],
                                                    x[self.DAYS_UNITS],
                                                    self.days_of_week[d],
                                                    "Yearly Goals"))
                res.append("{} {}".format("Generated by planning script",
                                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        res.append("\n")
        return res