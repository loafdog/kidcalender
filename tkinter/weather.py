import json
import requests
import os

class Forecast:

    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.forecast_filename = path + os.path.sep + 'forecast.json'
        self.conditions_filename = path + os.path.sep + 'conditions.json'

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
    
    def get_current_temp(self):
        c = self.conditions()
        cur_temp = int(c['current_observation']['temp_f'])
        return cur_temp

    def get_current_conditions(self):
        f = self.forecast()
        cond = f['forecast']['simpleforecast']['forecastday'][0]['conditions']
        return cond
