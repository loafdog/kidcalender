import pdb
import json
import requests
import os
import datetime as dt

import logging
logger = logging.getLogger(__name__)

class Forecast():

    def __init__(self, config):
        
        self.api_key = config['darksky']['api_key']
        self.lat_long = config['darksky']['lat_long']
        
        path = os.path.dirname(os.path.abspath(__file__))
        if self.api_key == "NONE":
            logging.warn("api_key={}. Running in SAMPLE mode".format(self.api_key))
            self.forecast_filename = path + os.path.sep + 'sample_forecast.json'
            self.yesterday_forecast_filename = path + os.path.sep + 'sample_yesterday_forecast.json'
        else:
            self.forecast_filename = path + os.path.sep + 'forecast.json'
            self.yesterday_forecast_filename = path + os.path.sep + 'yesterday_forecast.json'
        
    def read_forecast(self):
        forecast_data = None
        #logging.debug("Reading forecast file: %s" % self.forecast_filename)
        with open(self.forecast_filename, 'r') as f:
            forecast_data = json.load(f)
            
        return forecast_data

    def write_forecast(self, forecast_data):
        with open(self.forecast_filename, 'w') as f:
            logging.debug("Writing forecast file: %s" % self.forecast_filename)
            json_str = json.dumps(forecast_data, indent=4, sort_keys=True)
            f.write(json_str)
            
    def forecast_api(self):
        r = None
        try:
            resp = requests.get(
                'https://api.darksky.net/forecast/{}/{}'\
                .format(self.api_key, self.lat_long))
        except (requests.ConnectTimeout, requests.HTTPError,
                requests.ReadTimeout, requests.Timeout,
                requests.ConnectionError) as ex:
            logging.error("Exception in forcast_api", ex)
        else:
            if resp.ok:
                r = json.loads(resp.content.decode())
            else:
                logging.error('Failed to get forecast: {} {}'.format(resp.status_code, resp.text))
        return r

    def read_yesterday_forecast(self):
        forecast_data = None
        #logging.debug("Reading yesterday forecast file: %s" % self.yesterday_forecast_filename)
        try:
            with open(self.yesterday_forecast_filename, 'r') as f:
                forecast_data = json.load(f)
        except FileNotFoundError as ex:
            logging.error("yesterday file not found: {}".format(ex))
            return None
            
        return forecast_data

    def write_yesterday_forecast(self, forecast_data):
        with open(self.yesterday_forecast_filename, 'w') as f:
            logging.debug("Writing forecast file: %s" % self.yesterday_forecast_filename)
            json_str = json.dumps(forecast_data, indent=4, sort_keys=True)
            f.write(json_str)

    def yesterday_forecast_api(self):
        r = None
        try:
            now = dt.datetime.now()
            yesterday = now - dt.timedelta(hours=24)
            resp = requests.get(
                'https://api.darksky.net/forecast/{}/{},{}'\
                .format(self.api_key, self.lat_long, int(yesterday.timestamp())))
        except (requests.ConnectTimeout, requests.HTTPError,
                requests.ReadTimeout, requests.Timeout,
                requests.ConnectionError) as ex:
            logging.error("Exception in yesterdayforcast_api", ex)
        else:
            if resp.ok:
                r = json.loads(resp.content.decode())
            else:
                logging.error('Failed to get yesterday forecast: {} {}'.format(resp.status_code, resp.text))
        return r

    def forecast(self, update=False):
        if self.api_key == "NONE":
            return self.read_forecast()
        
        d = None
        if update == True:
            logging.debug("Update forecast, make api call")
            d = self.forecast_api()
            self.write_forecast(d)
        else:
            try:
                d = self.read_forecast()
            except:
                logging.warning("Failed to read forecast, make api call")
                d = self.forecast_api()
                self.write_forecast(d)
        return d

    def yesterday_forecast(self, update=False):
        if self.api_key == "NONE":
            return self.read_yesterday_forecast()
        
        d = None
        if update == True:
            logging.debug("Update forecast, make api call")
            d = self.yesterday_forecast_api()
            self.write_yesterday_forecast(d)
        else:
            try:
                d = self.read_yesterday_forecast()
            except:
                logging.warning("Failed to read forecast, make api call")
                d = self.yesterday_forecast_api()
                self.write_yesterday_forecast(d)
        return d


    def get_current_temp(self):
        f = self.forecast()
        if f == None:
            return 0
        cur_temp = f['currently']['temperature']
        return int(cur_temp)

    def get_high_temp(self):
        f = self.forecast()
        if f == None:
            return 0
        high = f['daily']['data'][1]['temperatureHigh']
        return int(high)

    def get_yesterday_high_temp(self):
        f = self.yesterday_forecast()
        if f == None:
            return 0
        return int(f['daily']['data'][0]['temperatureHigh'])

    def get_current_conditions(self):
        f = self.forecast()
        if f == None:
            return 'error'        
        cond = f['daily']['data'][0]['summary']
        return cond

    def _tomorrow_forecast(self):
        f = self.forecast()
        if f == None:
            return None

        now = dt.datetime.now()
        tomorrow = (now + dt.timedelta(hours=24)).date()
        
        fcast = dt.datetime.utcfromtimestamp(f['daily']['data'][1]['time']).date()
        if fcast > now.date() and fcast <= tomorrow:
            return f['daily']['data'][1]

        logging.debug("1 now={} tomorrow={} fcast={}".format(now, tommorrow, fcast))

        fcast = dt.datetime.utcfromtimestamp(f['daily']['data'][2]['time']).date()
        if fcast > now.date() and fcast <= tomorrow:
            return f['daily']['data'][2]

        logging.debug("2 now={} tomorrow={} fcast={}".format(now, tommorrow, fcast))
        logging.warning("Failed to find tomorrow forecast block")
        return None
    
    def get_tomorrow_high_temp(self):
        f = self._tomorrow_forecast()
        if f == None:
            return None

        return int(f['temperatureMax'])

    def get_tomorrow_conditions(self):
        f = self._tomorrow_forecast()
        if f == None:
            return None

        return f['summary']
    
    def update(self):
        self.forecast(update=True)
        self.yesterday_forecast(update=True)
