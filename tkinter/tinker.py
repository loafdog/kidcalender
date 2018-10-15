# TODO
#
# - text about temp being warm/cold/same as yesterday doesn't
#   work. says warmer when it was colder for example.
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
import weather
import thermometer

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.schedule = schedule.Schedule()
        self.weather = weather.Forecast()

        self.title("What is the weather today?")

        # This will set app to specific size
        #
        # Set this to adjust app window to size of screen you are using
        # self.width = 800
        # self.height = 400
        # self.geometry("{}x{}".format(self.width,self.height))

        # This will make app full screen and detect size
        # 
        self.attributes("-fullscreen", True)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        print("width: %d height: %d" % (self.width, self.height))
        
        self.bind("<Escape>", sys.exit)
        
        self.l_thermometer = thermometer.Thermometer(self, 100, self.height, 'current_temp')
        self.l_thermometer.frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.date_frame = tk.Frame(self)
        self.date_text = self.create_date(self.date_frame)

        self.weather_frame = tk.Frame(self)
        (self.feel_text, self.weather_text) = self.create_weather(self.weather_frame)

        self.kids = {}
        self.kid_frame_1 = tk.Frame(self)
        self.create_kid(self.kid_frame_1, self.kids, "Greta", "purple")


        self.kid_frame_2 = tk.Frame(self)
        self.create_kid(self.kid_frame_2, self.kids, "Cora", "pink")
       

        self.date_frame.pack(side=tk.TOP, fill=tk.X)
        self.weather_frame.pack(side=tk.TOP, fill=tk.X)
        self.kid_frame_1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.kid_frame_2.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        helv36 = font.Font(family='Helvetica', size=48, weight='bold')

        button_height = int(self.height/6)
        #self.button_frame = tk.Frame(self, height=button_height)
        self.button_frame = tk.Frame(self)
        
        #self.update_button = tk.Button(self.button_frame, text="TODAY", command=self.update)
        #self.update_button = tk.Button(self.button_frame, text="TODAY", command=self.update, height=200)
        self.update_button = tk.Button(self, text="TODAY", command=self.update, font=helv36, pady=20)
        #self.update_button = tk.Button(self.button_frame, text="TODAY", command=self.update, height=button_height, font=helv36)
        self.update_button.pack(side=tk.BOTTOM)
        self.button_frame.pack(side=tk.BOTTOM)
        
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
        
        kid_name_widget = tk.Label(frame, text=kid_name, bg=color, font=("Courier", name_font_size))
        kid_name_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        school_var = tk.StringVar()
        #school = self.schedule.get_weekly_school(kid_name)
        #kid_school_widget = tk.Label(frame, text=school, bg=color, font=("Courier", act_font_size))
        kid_school_widget = tk.Label(frame, textvariable=school_var, bg=color, font=("Courier", act_font_size))
        kid_school_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        kids[kid_name]['school_text'] = school_var

        act_var = tk.StringVar()
        #activity = self.schedule.get_weekly_activity(kid_name)
        #kid_activity_widget = tk.Label(frame, text=activity, bg=color, font=("Courier", act_font_size))
        kid_activity_widget = tk.Label(frame, textvariable=act_var, bg=color, font=("Courier", act_font_size))
        kid_activity_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        kids[kid_name]['act_text'] = act_var

    def update_feel(self):
        cur_temp = self.weather.get_high_temp()
        yesterday_temp = self.weather.get_yesterday_high_temp()

        if yesterday_temp == None:
            feel = "Yesterday high not available"
        elif cur_temp > yesterday_temp+5:
            feel = "Today temperature will be warmer than yesterday"
        elif cur_temp < yesterday_temp-5:
            feel = "Today termperature will be colder than yesterday"
        else:
            feel = "Today temperature will be same as yesterday"
        self.feel_text.set(feel)

    def update_weather(self):
        txt = self.weather.get_current_conditions()
        txt = "Today there may be: " + txt
        self.weather_text.set(txt)

    def update_date(self):
        date_str = self.schedule.get_date_str()
        day_str = self.schedule.get_day_str()
        txt = "Today is " + day_str + " " + date_str
        self.date_text.set(txt)

    def update_kid(self):
        for kid_name, texts in self.kids.items():
            school = self.schedule.get_weekly_school(kid_name)
            activity = self.schedule.get_weekly_activity(kid_name)
            texts['act_text'].set(activity)
            texts['school_text'].set(school)
            
    def update(self):
        self.weather.update()

        cur_temp = self.weather.get_current_temp()
        high_temp = self.weather.get_high_temp()
        self.l_thermometer.update(cur_temp, high_temp)

        self.schedule.update()

        self.update_date()
        self.update_feel()
        self.update_weather()
        self.update_kid()

if __name__ == "__main__":
    root = Root()
    root.mainloop()
