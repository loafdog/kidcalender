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
    day_to_num = {
        "monday":"0",
        "tuesday":"1",
        "wednesday":"2",
        "thursday":"3",
        "friday":"4",
        "saturday":"5",
        "sunday":"6"
    }
    
    num_to_day = {
        "0":"monday",
        "1":"tuesday",
        "2":"wednesday",
        "3":"thursday",
        "4":"friday",
        "5":"saturday",
        "6":"sunday"
    }
       
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.filename = path + os.path.sep + 'schedule.json'
        self.schedule_mtime = 0
        self.data = None
        self.read()


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

    def weekday_str(self):
        today = date.today()
        return Schedule.num_to_day[str(today.weekday())]

    def _get_weekly_by_key(self, kid, key):
        try:
            kid = self.data[kid.lower()]
        except KeyError as key:
            print(self.data)
            print("Key '%s' does not exist" % str(key))
            return "No kid {}".format(kid)

        try:
            weekly = kid["weekly"]
        except KeyError as key:
            print(kid)
            print("Key '%s' does not exist" % str(key))
            return "No weekly activities"

        try:
            days = weekly[key]
        except KeyError as key:
            print(weekly)
            print("Key '%s' does not exist" % str(key))
            return "No weekly {}".format(key)

        try:
            act = days[self.weekday_str()]
        except KeyError as key:
            print(days)
            print("Key '%s' does not exist" % str(key))
            return "No {} actvity".format(key)
        
        return act
    
    def get_weekly_school(self, kid):
        return self._get_weekly_by_key(kid, "school")
        
    def get_weekly_activity(self, kid):
        return self._get_weekly_by_key(kid, "activity")
                                       
    def get_day_str(self):
        today = date.today()
        day_str = calendar.day_name[today.weekday()]
        month_str = calendar.month_name[today.month]
        year = today.year
        day_str = "{0}".format(day_str)
        return day_str
    
    def get_date_str(self):
        today = date.today()
        month_str = calendar.month_name[today.month]
        year = today.year
        date_str = "{0} {1:%d} {2}".format(month_str, today, year)
        return date_str
