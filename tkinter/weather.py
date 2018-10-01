import pdb
import json
import requests
import os
from shutil import copy2

from datetime import date
from datetime import datetime, timezone

class Forecast:

    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.forecast_filename = path + os.path.sep + 'forecast.json'
        self.conditions_filename = path + os.path.sep + 'conditions.json'
        self.forecast_yesterday_filename = path + os.path.sep + 'forecast_yesterday.json'
        self.conditions_yesterday_filename = path + os.path.sep + 'conditions_yesterday.json'

        self.filename = path + os.path.sep + 'config.json'
        with open(self.filename, 'r') as f:
            print("Reading config file: %s" % self.filename)
            data = json.load(f)
            self.api_key = data['api_key']
            self.state = data['state']
            self.city = data['city']

    def read_forecast(self):
        forecast_data = None
        print("Reading forecast file: %s" % self.forecast_filename)
        with open(self.forecast_filename, 'r') as f:
            forecast_data = json.load(f)
            
        return forecast_data

    def write_forecast(self, forecast_data):
        with open(self.forecast_filename, 'w') as f:
            print("Writing forecast file: %s" % self.forecast_filename)
            json_str = json.dumps(forecast_data, indent=4, sort_keys=True)
            f.write(json_str)

    def read_conditions(self):
        conditions_data = None
        print("Reading conditions file: %s" % self.conditions_filename)
        with open(self.conditions_filename, 'r') as f:
            conditions_data = json.load(f)
            
        return conditions_data

    def write_conditions(self, conditions_data):
        with open(self.conditions_filename, 'w') as f:
            print("Writing conditions file: %s" % self.conditions_filename)
            json_str = json.dumps(conditions_data, indent=4, sort_keys=True)
            f.write(json_str)

    def read_yesterday_conditions(self):
        conditions_data = None
        print("Reading conditions file: %s" % self.conditions_yesterday_filename)
        try:
            with open(self.conditions_yesterday_filename, 'r') as f:
                conditions_data = json.load(f)
        except FileNotFoundError:
            return None

        return conditions_data


    def copy_to_yesterday(self, today_file_date, today_file, yesterday_file):
        # only copy to yesterday if today's date and date of
        # current/today file is if diff.

        # Read date from file: "7:00 PM EDT on September 26, 2018"
        # chop off time? or just get m/d/y from file?
        # convert str to date obj
        # get today date
        # if now > date_file then copy file

        #today = date.today()
        today = datetime.now(timezone.utc)
        if today > today_file_date:
            print("today {} is greater than forecast {} date".format(today, today_file_date))
            print("copying {} to {}".format(today_file, yesterday_file))
            copy2(today_file, yesterday_file)
            os.rename(today_file, today_file+'.bak')
        else:
            print("forecast {} is greater than or equal to today {} date".format(today_file_date, today))
        
        
    def forecast_api(self):
        r = None
        try:
            resp = requests.post(
                'http://api.wunderground.com/api/{}/forecast/q/{}/{}.json'\
                .format(self.api_key, self.state, self.city))
        except (requests.ConnectTimeout, requests.HTTPError,
                requests.ReadTimeout, requests.Timeout,
                requests.ConnectionError) as ex:
            print("Exception in forcast_api", ex)
        else:
            r = json.loads(resp.content.decode())
        return r

    def conditions_api(self):
        r = None
        try:
            resp = requests.post(
                'http://api.wunderground.com/api/{}/conditions/q/{}/{}.json'\
                .format(self.api_key, self.state, self.city))
        except (requests.ConnectTimeout, requests.HTTPError,
                requests.ReadTimeout, requests.Timeout,
                requests.ConnectionError) as ex:
            print("Exception in conditions_api", ex)
        else:
            r = json.loads(resp.content.decode())
        return r

    def update(self):
        f = self.forecast()
        fdate = f['forecast']['simpleforecast']['forecastday'][0]['date']
        fdate_obj = datetime.strptime("{}{}{}".format(fdate['month'],fdate['day'], fdate['year']), "%m%d%Y")
        fdate_obj = fdate_obj.replace(tzinfo=timezone.utc)
        self.copy_to_yesterday(fdate_obj, self.forecast_filename, self.forecast_yesterday_filename)

        c = self.conditions()
        cdate = c['current_observation']['observation_time_rfc822']
        cdate_obj = datetime.strptime(cdate, '%a, %d %b %Y %H:%M:%S %z')
        self.copy_to_yesterday(cdate_obj, self.conditions_filename, self.conditions_yesterday_filename)


    def forecast(self):
        d = None
        try:
            d = self.read_forecast()
        except:
            d = self.forecast_api()
            self.write_forecast(d)
        return d
    
    def conditions(self):
        c = None
        try:
            c = self.read_conditions()
        except:
            c = self.conditions_api()
            self.write_conditions(c)
        return c

    def yesterday_conditions(self):
        c = None
        try:
            c = self.read_yesterday_conditions()
        except RuntimeError as ex:
            print("Failed to read yesterday condtions: {}".format(ex))
            c = None
        return c

    def get_current_temp(self):
        c = self.conditions()
        cur_temp = int(c['current_observation']['temp_f'])
        return cur_temp

    def get_high_temp(self):
        f = self.forecast()
        temp = f['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
        return int(temp)

    def get_yesterday_temp(self):
        c = self.yesterday_conditions()
        if c == None:
            return None
        temp = int(c['current_observation']['temp_f'])
        return temp
        
    def get_current_conditions(self):
        f = self.forecast()
        cond = f['forecast']['simpleforecast']['forecastday'][0]['conditions']
        return cond

    def get_tomorrow_conditions(self):
        pass

    def get_yesterday_conditions(self):
        # useful?
        pass
