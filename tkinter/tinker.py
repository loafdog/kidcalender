# TODO
#
# - add ability to check what temp will be tommorrow vs today
#
# - automatically update at 5am for today.

import tkinter as tk
from tkinter import font

from datetime import date
import calendar
import json
import requests
import os
import sys
import pdb

import schedule
import weather.weather as weather
import thermometer

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="pyweathercal.log",
    level=logging.DEBUG,
#    format="%(asctime)s:%(levelname)s:%(lineno)3s:%(message)s"
#    format="%(asctime)s:%(levelname)s:%(lineno)3s:%(funcName)s:%(message)s"
    format="%(asctime)s:%(filename)s:%(lineno)3s:%(funcName)30s: %(message)s"
    )

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        # Assume all conf/schedule files are in same dir as app
        path = os.path.dirname(os.path.abspath(__file__))

        if os.path.isfile(path + os.path.sep + 'config.json'):
            self.filename = path + os.path.sep + 'config.json'
        elif os.path.isfile(path + os.path.sep + 'sample_config.json'):
            self.filename = path + os.path.sep + 'sample_config.json'
            logging.warning("Running in SAMPLE mode. Found {}".format(self.filename))
        else:
            logging.critical("Failed to find a config.json or sample_config.json file in {}".format(path))
            exit(1)

        # logging.debug('Test debug')
        # logging.info('Test info')
        # logging.warning('Test warning')
        # logging.error('Test error')
        # logging.critical('Test critical')
        
        with open(self.filename, 'r') as f:
            logging.debug("Reading config file: %s" % self.filename)        
            self.config = json.load(f)
            logging.debug("{}".format(self.config))

        self.schedule = schedule.Schedule()
        self.weather = weather.Weather(self.config)
        
        self.title(self.config['title'])

        if self.config['full_screen']:
            # This will make app full screen and detect size
            # 
            self.attributes("-fullscreen", True)
            self.width = self.winfo_screenwidth()
            self.height = self.winfo_screenheight()
        else:
            # This will set app to specific size
            #
            self.attributes("-fullscreen", False)
            self.width = self.config['width']
            self.height = self.config['height']
            self.geometry("{}x{}".format(self.width,self.height))

        logging.debug("width: %d height: %d" % (self.width, self.height))

        self.bind("<Escape>", sys.exit)
        
        self.l_thermometer = thermometer.Thermometer(self, 100, self.height, 'current_temp')
        self.l_thermometer.frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.date_frame = tk.Frame(self)
        self.date_text = self.create_date(self.date_frame)

        self.weather_frame = tk.Frame(self)
        (self.feel_text, self.weather_text) = self.create_weather(self.weather_frame)

        self.date_frame.pack(side=tk.TOP, fill=tk.X)
        self.weather_frame.pack(side=tk.TOP, fill=tk.X)

        self.kids = {}
        for kid in self.schedule.kids():
            f = tk.Frame(self)
            self.create_kid(f, self.kids, kid, self.schedule.color(kid))
            f.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        # Custom button size is hard...            
        button_font = font.Font(family='Helvetica', size=28, weight='bold')

        self.button_frame = tk.Frame(self)

        self.update_button = tk.Button(self.button_frame, text="TODAY", command=self.update, font=button_font, pady=20)
        self.update_tomorrow_button = tk.Button(self.button_frame, text="TOMORROW", command=self.update_tomorrow, font=button_font, pady=20)

        self.update_tomorrow_button.pack(side=tk.RIGHT)
        self.update_button.pack(side=tk.RIGHT)
        
        self.button_frame.pack(side=tk.BOTTOM)

        # Auto update when app starts
        self.update()

    def create_date(self, frame):
        font_size = 20
        date_var = tk.StringVar()
        date_widget = tk.Label(frame, textvariable=date_var, bg="gray", font=("Courier", font_size))
        date_widget.pack(side=tk.TOP, fill=tk.X)
        return date_var

    def create_weather(self, frame):
        font_size = 20
        feel_var = tk.StringVar()
        feel_widget = tk.Label(frame, textvariable=feel_var, bg="gray", font=("Helvetica", font_size))
        feel_widget.pack(side=tk.TOP, fill=tk.X)

        weather_var = tk.StringVar()
        weather_widget = tk.Label(frame, textvariable=weather_var, bg="gray", font=("Mono", font_size))
        weather_widget.pack(side=tk.TOP, fill=tk.X)

        return (feel_var, weather_var)
        
    def create_kid(self, frame, kids, kid_name, color):
        name_font_size = 34
        act_font_size = 24

        kids[kid_name] = {}
        
        kid_name_widget = tk.Label(frame, text=kid_name.capitalize(), bg=color, font=("Courier", name_font_size))
        kid_name_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        school_var = tk.StringVar()
        kid_school_widget = tk.Label(frame, textvariable=school_var, bg=color, font=("Courier", act_font_size))
        kid_school_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        kids[kid_name]['school_text'] = school_var

        act_var = tk.StringVar()
        kid_activity_widget = tk.Label(frame, textvariable=act_var, bg=color, font=("Courier", act_font_size))
        kid_activity_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        kids[kid_name]['act_text'] = act_var

    def update_feel(self, txt):
        self.feel_text.set(txt)

    def update_weather(self, txt):
        self.weather_text.set(txt)

    def update_date(self, txt):
        self.date_text.set(txt)

    def update_kid(self, tomorrow=False):
        for kid_name, texts in self.kids.items():
            school = self.schedule.get_weekly_school(kid_name, tomorrow)
            activity = self.schedule.get_weekly_activity(kid_name, tomorrow)
            texts['act_text'].set(activity)
            texts['school_text'].set(school)
            
    def update(self):
        self.weather.update()

        cur_temp = self.weather.current_temp()
        high_temp = self.weather.high_temp()
        self.l_thermometer.update(cur_temp, high_temp)

        self.schedule.update()

        date_str = self.schedule.get_date_str()
        day_str = self.schedule.get_day_str()
        txt = "Today is " + day_str + " " + date_str
        self.update_date(txt)
        
        txt = self.weather.feel()
        self.update_feel(txt)
        txt = self.weather.condition()
        self.update_weather(txt)
        self.update_kid()
        
    def update_tomorrow(self):
        self.weather.update()

        high_temp = self.weather.tomorrow_high_temp()
        self.l_thermometer.update(None, high_temp)

        self.schedule.update()

        date_str = self.schedule.get_tomorrow_date_str()
        day_str = self.schedule.get_tomorrow_day_str()
        txt = "Tomorrow is " + day_str + " " + date_str
        self.update_date(txt)
        
        txt = self.weather.tomorrow_feel()
        self.update_feel(txt)
        txt = self.weather.tomorrow_condition()
        self.update_weather(txt)
        self.update_kid(tomorrow=True)

if __name__ == "__main__":
    root = Root()
    root.mainloop()
