import os
import json
from datetime import date
import calendar

class Schedule:
    """Manage schedule details
    Read in schedule from schedule file.
    Update schedule when schedule file changes
    Stuff...
    """

    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.filename = path + os.path.sep + 'schedule.json'
        self.schedule_mtime = 0
        self.data = None
        self.read()

        self.wear_days = {
        "Gym" : {
            80 : ["shorts/t-shirt"],
            50 : ["pants/long-sleeve shirt"],
            0 :  ["warm pants","sweat-shirt/sweater"]
        },
        "Any" : {
            80 : ["skirt/t-shirt","summer dress"],
            60 : ["dress with shorts","t-shirt"],
            40 : ["dress with pants","long-sleeve shirt"],
            0 :  ["warm pants","sweat-shirt/sweater"]
        }
    }


    def update(self):
        """Update schedule data if schedule file changed
        """
        if self.data == None\
           or self.schedule_mtime != os.path.getmtime(self.filename):
            self.read()

    def read(self):
        """Read data from schedule file
        """
        with open(self.filename, 'r') as f:
            print("Reading schedule file: %s" % self.filename)
            self.data = json.load(f)
            self.schedule_mtime = os.path.getmtime(self.filename)


    def get_wear_day(kid, cur_temp):
        today = date.today()

        weekday_str = self.data["num_to_day"][str(today.weekday())]

        week_days = self.data[kid]["weekly"]
        activity = week_days[weekday_str]
        ranges = self.wear_days.get(activity, wear_days["Any"])
        wear = None
        for k in sorted(ranges):
            if cur_temp >= k:
                wear = ranges[k]
                break
        return wear

    def get_activity(self, kid):
        today = date.today()

        weekday_str = self.data["num_to_day"][str(today.weekday())]

        week_days = self.data[kid]["weekly"]

        if weekday_str in week_days["school"]:
            school_act = week_days["school"][weekday_str]
        else:
            school_act = None

        if weekday_str in week_days["activity"]:
            after_school_act = week_days["activity"][weekday_str]
        else:
            after_school_act = None

        act = self.get_schedule_date()
        if act == None:
            print("No activity found for {0} on {1}".format(kid,today))
            activity = [school_act, after_school_act]
        else:
            activity = act["lines"]
            # print("ACT", act["school"])
            # if "no" == act["school"]:
            #     #activity = "{0}\n{1}".format("NO SCHOOL", act["name"])
            #     activity = [act["name"], "NO SCHOOL"]
            # else:
            #     #activity = "{0}\n{1}".format(school_act, act["name"])
            #     school_act = week_days["school"][weekday_str]
            #     activity = [school_act, act["name"]]

        return activity

    def get_schedule_date(self):
        today = date.today()
        key = today.strftime("%m/%d/%Y")
        print("KEY", key)
        print(self.data["dates"])
        # print(self.data["dates"][key])
        if key in self.data["dates"]:
            return self.data["dates"][key]
        return None

    def get_what_to_wear(self, kid, cur_temp):
        today = date.today()
        wear = ""
        weekday_str = self.data["num_to_day"][str(today.weekday())]
        week_days = self.data[kid]["weekly"]
        print("KID what to wear: ", kid, week_days)
        act = week_days["school"][weekday_str]
        ranges = self.wear_days.get(act, self.wear_days["Any"])
        wear = None
        for k in sorted(ranges):
            if cur_temp >= k:
                wear = ranges[k]
                break
        return wear

    def get_day_info(self):
        today = date.today()
        day_str = calendar.day_name[today.weekday()]
        month_str = calendar.month_name[today.month]
        year = today.year
        day_str = "{0}".format(day_str)
        date_str = "{0} {1:%d} {2}".format(month_str, today, year)
        return day_str,date_str
