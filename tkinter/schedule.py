import os
import json
import datetime as dt
import calendar

import logging
logger = logging.getLogger(__name__)

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

        if os.path.isfile(path + os.path.sep + 'schedule.json'):
            self.filename = path + os.path.sep + 'schedule.json'
        elif os.path.isfile(path + os.path.sep + 'sample_schedule.json'):
            self.filename = path + os.path.sep + 'sample_schedule.json'
            logging.warn("Running in SAMPLE mode. Found {}".format(self.filename))
        else:
            logging.error("Failed to find a schedule.json or sample_schedule.json file in {}".format(path))
        
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
            logger.debug("Reading schedule file: %s" % self.filename)
            self.data = json.load(f)
            self.schedule_mtime = os.path.getmtime(self.filename)

    def kids(self):
        k = self.data.keys()
        logger.debug("kids: %s" % k)
        return k

    def color(self, kid):
        return self.data[kid.lower()]['color']

    def weekday_str(self, tomorrow=False):
        if tomorrow:
            today = dt.date.today() + dt.timedelta(days=1)
        else:
            today = dt.date.today()
        return Schedule.num_to_day[str(today.weekday())]

    def _get_weekly_by_key(self, kid, key, tomorrow=False):
        try:
            kid = self.data[kid.lower()]
        except KeyError as key:
            logging.error(self.data)
            logging.error("Key '%s' does not exist" % str(key))
            return "No kid {}".format(kid)

        try:
            weekly = kid["weekly"]
        except KeyError as key:
            logging.error(kid)
            logging.error("Key '%s' does not exist" % str(key))
            return "No weekly activities"

        try:
            days = weekly[key]
        except KeyError as key:
            logging.error(weekly)
            logging.error("Key '%s' does not exist" % str(key))
            return "No weekly {}".format(key)

        try:
            act = days[self.weekday_str(tomorrow)]
        except KeyError as key:
            logging.error(days)
            logging.error("Key '%s' does not exist" % str(key))
            return "No {} actvity".format(key)
        
        return act
    
    def get_weekly_school(self, kid, tomorrow=False):
        return self._get_weekly_by_key(kid, "school", tomorrow)
        
    def get_weekly_activity(self, kid, tomorrow=False):
        return self._get_weekly_by_key(kid, "activity", tomorrow)
                                       
    def get_day_str(self):
        today = dt.date.today()
        day_str = calendar.day_name[today.weekday()]
        month_str = calendar.month_name[today.month]
        year = today.year
        day_str = "{0}".format(day_str)
        return day_str
    
    def get_date_str(self):
        today = dt.date.today()
        month_str = calendar.month_name[today.month]
        year = today.year
        date_str = "{0} {1:%d} {2}".format(month_str, today, year)
        return date_str

    def get_tomorrow_day_str(self):
        tomorrow = dt.date.today() + dt.timedelta(days=1)
        day_str = calendar.day_name[tomorrow.weekday()]
        month_str = calendar.month_name[tomorrow.month]
        year = tomorrow.year
        day_str = "{0}".format(day_str)
        return day_str
    
    def get_tomorrow_date_str(self):
        tomorrow = dt.date.today() + dt.timedelta(days=1)
        month_str = calendar.month_name[tomorrow.month]
        year = tomorrow.year
        date_str = "{0} {1:%d} {2}".format(month_str, tomorrow, year)
        return date_str
    
