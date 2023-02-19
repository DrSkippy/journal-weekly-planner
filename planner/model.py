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
                if row[0].startswith("#"):
                    continue
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
    UNITS_COUNT = "count"

    ACTIVITY_NAME = 0
    ACTIVITY_TIME = 2
    ACTIVITY_UNITS = 3

    DAYS_ACTIVITY = 0
    DAYS_DAILY_TIME = 1
    DAYS_UNITS = 2

    PAGE_ROWS = 58

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

    def hours_format_units(self, x, unit):
        fmt = "{:4} {:3}"
        if unit == self.UNITS_HOUR:
            if x < 0.0334:
                val, ustring = int(x*3600), "sec"
            elif x < 2:
                val, ustring = int(x * 60), "min"
            else:
                val, ustring = round(x, 1), "hrs"
        elif unit == self.UNITS_COUNT:
            val, ustring = int(x), "cnt"
        else:
            # display provided... must be 3 char
            val, ustring = int(x), unit[:3]
        return fmt.format(val, ustring)

    def add_activity(self, activity, days, weekly_time):
        self.activity_list.add(activity[0])
        if len(days) > 0 and days[0] == "a":
            # all days of week
            days = list(self.days_of_week.keys())
        n = len(days)
        for d in days:
            if activity[self.ACTIVITY_UNITS] == self.UNITS_HOUR:
                # hours split over days
                daily_time = float(weekly_time) / n
            else:
                # count per session
                daily_time = float(weekly_time)
            daily_time = round(daily_time, 2)
            self.days[d].append((activity[self.ACTIVITY_NAME],
                                 daily_time,
                                 activity[self.ACTIVITY_UNITS]))

    def plan_paper(self):
        res = ["<hr>"]
        for d in self.days:
            res.append(self.days_of_week[d])
            res.append("<hr>")
            for x in self.days[d]:
                value_display_str = self.hours_format_units(x[self.DAYS_DAILY_TIME], x[self.DAYS_UNITS])
                res.append("{:13} ({}): __________".format(x[self.DAYS_ACTIVITY], value_display_str))
            res.append("<hr>")
        return res

    def plan_paper_week_days(self, date_obj=None):
        res = ["<pre>" ]
        fmt = "{:13}" + "| {:16}" * 7
        res.append(fmt.format(*tuple([" "] + list(self.sunday_start(date_obj).values()))))
        res.append(fmt.format(*tuple(["Activity"] + [self.days_of_week[i] for i in self.days_of_week])))
        res.append("<hr>")
        for activity in self.activity_list:
            row = ["{:13}".format(activity)]
            for d in self.days:
                for x in self.days[d]:
                    if x[self.DAYS_ACTIVITY] == activity:
                        value_display_str = self.hours_format_units(x[self.DAYS_DAILY_TIME], x[self.DAYS_UNITS])
                        row.append("{}: _______".format(value_display_str))
                        break
                else:
                    row.append(" " * 17)
            res.append(fmt.format(" " * 13, *[" " * 16 for i in range(7)]))
            res.append("|".join(row))
        res.append("<hr>")
        # score box
        res.append(fmt.format(" " * 13, *["   |         " for i in range(7)]))
        res.append(fmt.format(" " * 13, *["   |         " for i in range(7)]))
        res.append(fmt.format(" " * 13, *["---           " for i in range(7)]))
        # fill to end of page
        for i in range(self.PAGE_ROWS-len(res) - 2):
            res.append(fmt.format(*[" "]*8))
        res.append("</pre>\n")
        return res

    def sunday_start(self, date_obj=None):
        if date_obj is not None:
            today = date_obj
        else:
            today = datetime.date.today()
        # sunday = 6
        sunday = today + datetime.timedelta((6 - today.weekday()) % 7)
        print("Running tasks for week plan on {}, generating Nozbe tasks starting {}".format(today, sunday))
        dated_dow = {}
        for i, k in enumerate(self.days_of_week.keys()):
            _date = sunday + datetime.timedelta(i)
            dated_dow[k] = _date.strftime("%B %-d")
        return dated_dow

    def plan_nozbe(self, date_obj=None):
        dow_dict = self.sunday_start(date_obj)
        res = []
        for d in self.days:
            for x in self.days[d]:
                value_display_str = self.hours_format_units(x[self.DAYS_DAILY_TIME], x[self.DAYS_UNITS])
                res.append(
                    ". {} for {} #{} #{}".format(x[self.DAYS_ACTIVITY],
                                                 value_display_str,
                                                 # self.days_of_week[d],
                                                 dow_dict[d],
                                                 "Yearly Goals"))
                res.append("{} {}".format("Generated by planning script",
                                          datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        res.append("\n")
        return res
