import weather.darksky.weather_darksky

import logging
logger = logging.getLogger(__name__)


class Weather():

    def __init__(self, config):
        if 'darksky' in config:
            logging.debug("Loading darksky")
            self.forecast = weather.darksky.weather_darksky.Forecast(config)
        elif 'wunderground' in config:
            logging.debug("Loading wunderground")
            self.forecast = weather.wunderground.weather.Forecast(config)
        else:
            raise 'No weather api keys found in config'


    def forecast(self):
        # return Forecast class?
        logging.debug("here")

    def update(self):
        self.forecast.update()

    def feel(self):
        cur_temp = self.forecast.get_high_temp()
        yesterday_temp = self.forecast.get_yesterday_high_temp()
        logging.debug("high: today {}  yesterday {}".format(cur_temp, yesterday_temp))
        if yesterday_temp == None:
            feel = "Yesterday high not available"
        elif cur_temp > yesterday_temp+3:
            feel = "Today will be warmer than yesterday"
        elif cur_temp < yesterday_temp-3:
            feel = "Today will be colder than yesterday"
        else:
            feel = "Today temperature will be same as yesterday"
        return feel

    def condition(self):
        txt = self.forecast.get_current_conditions()
        txt = "Conditions: " + txt
        return txt

    def current_temp(self):
        return self.forecast.get_current_temp()

    def high_temp(self):
        return self.forecast.get_high_temp()

    def tomorrow_high_temp(self):
        return self.forecast.get_tomorrow_high_temp()
    
    def tomorrow_condition(self):
        txt = self.forecast.get_tomorrow_conditions()
        txt = "Conditions: " + txt
        return txt

    def tomorrow_feel(self):
        tomorrow_temp = self.forecast.get_tomorrow_high_temp()
        cur_temp = self.forecast.get_high_temp()
        logging.debug("high: today {}  tomorrow {}".format(cur_temp, tomorrow_temp))
        if tomorrow_temp == None:
            feel = "Tomorrow high not available"
        elif tomorrow_temp > cur_temp + 3:
            feel = "Tomorrow will be warmer than today"
        elif tomorrow_temp < cur_temp-3:
            feel = "Tomorrow will be colder than today"
        else:
            feel = "Tomorrow temperature will be same as today"
        return feel
