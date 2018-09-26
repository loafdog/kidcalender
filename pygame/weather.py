import pygame
import os
import time
import threading
import json
import requests

class Forecast:

    forecast_mtime = 0
    forecast_filename = None
    conditions_filename = None
    forecast_data = None
    conditions_data = None

    # how often to update the forecast by going to remote weather
    # API. in seconds
    api_update_interval = 60*60
    
    def __init__(self):
        self.run_update = False
        self.update_thread = None
        self.timer_cond = threading.Condition()
        
        path = os.path.dirname(os.path.abspath(__file__))
        self.forecast_filename = path + os.path.sep + 'forecast.json'
        self.conditions_filename = path + os.path.sep + 'conditions.json'

        path = os.path.dirname(os.path.abspath(__file__))
        self.filename = path + os.path.sep + 'config.json'
        with open(self.filename, 'r') as f:
            print("Reading config file: %s" % self.filename)
            data = json.load(f)
            self.api_key = data['api_key']
            self.state = data['state']
            self.city = data['city']

        self.update()

    def forecast_api(self, bad=''):
        r = None
        try:
            resp = requests.post(
                'http://{}api.wunderground.com/api/{}/forecast/q/{}/{}.json'\
                .format(bad, self.api_key, self.state, self.city))
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

    def read_forecast(self):
        print("Reading forecast file: %s" % self.forecast_filename)
        with open(self.forecast_filename, 'r') as f:
            self.forecast_data = json.load(f)

        print("Reading conditions file: %s" % self.conditions_filename)
        with open(self.conditions_filename, 'r') as f:
            self.conditions_data = json.load(f)

    # Use this to hit the weather API and update the forecast file. Call
    # from thread that will update set interval.
    def update(self, bad=''):
        local_mtime = self.forecast_mtime

        tmp = self.forecast_api(bad)
        if tmp != None:
            self.forecast_data = tmp
            with open(self.forecast_filename, 'w') as f:
                print("Writing forecast file: %s" % self.forecast_filename)
                json_str = json.dumps(self.forecast_data, indent=4, sort_keys=True)
                f.write(json_str)
                local_mtime = os.path.getmtime(self.forecast_filename)
                self.forecast_mtime = local_mtime
                
        tmp = self.conditions_api()
        if tmp != None:
            self.conditions_data = tmp
            with open(self.conditions_filename, 'w') as f:
                print("Writing conditions file: %s" % self.conditions_filename)
                json_str = json.dumps(self.conditions_data, indent=4,
                                      sort_keys=True)
                f.write(json_str)
                local_mtime = os.path.getmtime(self.conditions_filename)
            

    def update_display(self):
        print("Posting forecast update display event")
        ev = pygame.event.Event(pygame.USEREVENT, {'data': 'forecast'})
        pygame.event.post(ev)

    def throw_except(self):
        raise
        try:
            resp = requests.post(
                'http://sapi.wunderground.com/api/{}/forecast/q/{}/{}.json'\
                .format(self.api_key, self.state, self.city))
        except (requests.ConnectTimeout, requests.HTTPError,
                requests.ReadTimeout, requests.Timeout,
                requests.ConnectionError) as ex:
            print("Exception in throw_except", ex)

        
    def timed_update(self, bad=''):
        print('Check if forecast needs update')
        try:
            if self.forecast_mtime == 0:
                self.forecast_mtime = os.path.getmtime(self.forecast_filename)
        except:
            print("forecast file not found, creating: " % self.forecast_filename)
            self.update()
            self.update_display()

        else:
#            if time.time() - self.forecast_mtime > self.api_update_interval:
            if True:
                print("Forecast needs update")
                print("Timer updating forecast/conditon files: %s" % self.forecast_filename)
                self.update(bad)
                self.update_display()
        
    def update_timer(self):
        while self.run_update:
            self.timed_update()
            self.timer_cond.acquire()
            self.timer_cond.wait(self.api_update_interval)
            self.timer_cond.release()
            
    def start_update_timer(self):
        self.run_update = True
        self.update_thread = threading.Thread(target = self.update_timer)
        self.update_thread.start()

    def stop_update_timer(self):
        if self.update_thread != None:
            print('Stopping forecast update timer')
            self.timer_cond.acquire()
            self.run_update = False
            self.timer_cond.notify()
            self.timer_cond.release()
            self.update_thread.join()
            print('Forecast update timer stopped')
        
    def forecast_temp(self):
        today = self.forecast_data['forecast']['simpleforecast']['forecastday'][0]
        #return (today['high']['fahrenheit'], today['conditions'])
        return int(today['high']['fahrenheit'])

    def high_temp(self):

        today = self.forecast_data['forecast']['simpleforecast']['forecastday'][0]
        return (today['high']['fahrenheit'], today['conditions'])

    def current_temp(self):
        self.read_forecast()
        print("current_temp: ",int(self.conditions_data['current_observation']['temp_f']))
        return int(self.conditions_data['current_observation']['temp_f'])
