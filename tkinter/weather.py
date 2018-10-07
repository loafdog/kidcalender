import pdb
import json
import requests
import os
from shutil import copy2

import datetime as dt
# from dt import date
# from dt import dt, timezone, timedelta

class Forecast:

    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.forecast_filename = path + os.path.sep + 'forecast.json'
        self.conditions_filename = path + os.path.sep + 'conditions.json'
        self.yesterday_forecast_filename = path + os.path.sep + 'yesterday_forecast.json'
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
        #print("Reading forecast file: %s" % self.forecast_filename)
        with open(self.forecast_filename, 'r') as f:
            forecast_data = json.load(f)
            
        return forecast_data

    def read_yesterday_forecast(self):
        forecast_data = None
        #print("Reading yesterday forecast file: %s" % self.yesterday_forecast_filename)
        try:
            with open(self.yesterday_forecast_filename, 'r') as f:
                forecast_data = json.load(f)
        except FileNotFoundError as ex:
            print("yesterday file not found: {}".format(ex))
            return None
            
        return forecast_data

    def write_forecast(self, forecast_data):
        with open(self.forecast_filename, 'w') as f:
            print("Writing forecast file: %s" % self.forecast_filename)
            json_str = json.dumps(forecast_data, indent=4, sort_keys=True)
            f.write(json_str)

    def read_conditions(self):
        conditions_data = None
        #print("Reading conditions file: %s" % self.conditions_filename)
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
        #print("Reading yesterday conditions file: %s" % self.conditions_yesterday_filename)
        try:
            with open(self.conditions_yesterday_filename, 'r') as f:
                conditions_data = json.load(f)
        except FileNotFoundError as ex:
            print("yesterday file not found: {}".format(ex))
            return None

        return conditions_data


    def copy_forecast_to_yesterday(self):
        # only copy to yesterday if today's date and date of
        # current/today file is diff. Looks like forecast gets updated
        # once per day at 7pm?  Any case, at midnight it will change
        # date to next day.

        # Read parts of date from file and build datetime obj
        # Get date from datetime
        # get today date
        # if now_date > file_date then copy file

        f = self.forecast()
        fdate = f['forecast']['simpleforecast']['forecastday'][0]['date']
        dt_obj = dt.datetime.strptime("{}{}{}".format(fdate['month'],fdate['day'], fdate['year']), "%m%d%Y")
        fdate_obj = dt_obj.date()

        today = dt.datetime.now().date()
        if today > fdate_obj:
            print("today {} is greater than forecast {} date".format(today, fdate_obj))
            print("copying {} to {}".format(self.forecast_filename, self.yesterday_forecast_filename))
            copy2(self.forecast_filename, self.yesterday_forecast_filename)
        else:
            print("forecast {} is greater than or equal to today {} date".format(fdate_obj, today))
            print("skip copying {} to {}".format(self.forecast_filename, self.yesterday_forecast_filename))
        
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
        self.forecast(update=True)        
        self.copy_forecast_to_yesterday()

        
        # c = self.conditions()
        # cdate = c['current_observation']['observation_time_rfc822']
        # cdate_obj = dt.datetime.strptime(cdate, '%a, %d %b %Y %H:%M:%S %z')
        # self.copy_to_yesterday(cdate_obj, self.conditions_filename, self.conditions_yesterday_filename)
        

    def forecast(self, update=False):
        d = None
        if update == True:
            print("Update forecast, make api call")
            d = self.forecast_api()
            self.write_forecast(d)
        else:
            try:
                d = self.read_forecast()
            except:
                print("Failed to read forecast, make api call")
                d = self.forecast_api()
                self.write_forecast(d)
        return d

    def yesterday_forecast(self):
        d = self.read_yesterday_forecast()
        return d

    def conditions(self):
        c = None
        try:
            c = self.read_conditions()
            # cdate = c['current_observation']['observation_time_rfc822']
            # cdate_obj = dt.datetime.strptime(cdate, '%a, %d %b %Y %H:%M:%S %z')
            cdate_obj = dt.datetime.fromtimestamp(os.path.getmtime(self.conditions_filename))
            #pdb.set_trace()
            if dt.datetime.now() > cdate_obj + dt.timedelta(hours=1) :
                print("Calling conditions_api last call {}".format( cdate_obj))
                c = self.conditions_api()
                self.write_conditions(c)
        except Exception as ex:
            print(ex)
            c = self.conditions_api()
            self.write_conditions(c)
        return c

    def yesterday_conditions(self):
        c = None
        try:
            c = self.read_yesterday_conditions()
        #except RuntimeError as ex:
        except Exception as ex:
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

    def get_yesterday_high_temp(self):
        f = self.yesterday_forecast()
        if f == None:
            return None
        temp = f['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
        return int(temp)

    
    # def get_yesterday_temp(self):
    #     c = self.yesterday_conditions()
    #     if c == None:
    #         print("No temp for yesterday")
    #         return None
    #     temp = int(c['current_observation']['temp_f'])
    #     return temp
        
    def get_current_conditions(self):
        f = self.forecast()
        cond = f['forecast']['simpleforecast']['forecastday'][0]['conditions']
        return cond

    def get_tomorrow_conditions(self):
        pass

    def get_yesterday_conditions(self):
        # useful?
        pass
