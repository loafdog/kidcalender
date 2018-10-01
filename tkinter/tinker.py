import tkinter as tk

from datetime import date
import calendar
import json
import requests
import os
import pdb
import schedule
import weather
import thermometer

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.schedule = schedule.Schedule()
        self.weather = weather.Forecast()

        self.width = 800
        self.height = 400
        
        self.title("Thermometer")
        self.geometry("{}x{}".format(self.width,self.height))


        # self.l_thermometer_frame = tk.Frame(self)
        # self.l_thermometer = self.create_thermometer(self.l_thermometer_frame, 100, self.height)

        # self.r_thermometer_frame = tk.Frame(self)
        # self.r_thermometer = self.create_thermometer(self.r_thermometer_frame, 100, self.height)
        self.l_thermometer = thermometer.Thermometer(self, 100, self.height, 'current_temp')

        self.date_frame = tk.Frame(self)
        self.create_date(self.date_frame)

        self.weather_text = None
        self.weather_frame = tk.Frame(self)
        self.create_weather(self.weather_frame, self.weather_text)

        self.kids = {}
        self.kid_frame_1 = tk.Frame(self)
        self.create_kid(self.kid_frame_1, self.kids, "Greta", "purple")

        self.kid_frame_2 = tk.Frame(self)
        self.create_kid(self.kid_frame_2, self.kids, "Cora", "pink")

        self.l_thermometer.frame.pack(side=tk.LEFT, fill=tk.Y)
        
        #self.r_thermometer_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.date_frame.pack(side=tk.TOP, fill=tk.X)
        self.weather_frame.pack(side=tk.TOP, fill=tk.X)
        self.kid_frame_1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.kid_frame_2.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.update_button = tk.Button(self, text="UPDATE", command=self.update)
        self.update_button.pack(side=tk.BOTTOM)

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
        date_str = self.schedule.get_date_str()
        day_str = self.schedule.get_day_str()

        txt = "Today is " + day_str + " " + date_str

        date_widget = tk.Label(frame, text=txt, bg="gray")
        date_widget.pack(side=tk.TOP, fill=tk.X)

        # date_widget = tk.Label(frame, text=date_str, bg="gray")
        # date_widget.pack(side=tk.TOP, fill=tk.X)
        
        # day_widget = tk.Label(frame, text=day_str, bg="gray")
        # day_widget.pack(side=tk.TOP, fill=tk.X)
        

    def create_weather(self, frame, weather):
        cur_temp = self.weather.get_current_temp()
        yesterday_temp = self.weather.get_yesterday_temp()

        if yesterday_temp == None:
            feel = ""
        elif cur_temp > yesterday_temp+5:
            feel = "Today will be warmer than yesterday"
        elif cur_temp < yesterday_temp-5:
            feel = "Today will be colder than yesterday"
        else:
            feel = "Today will be same as yesterday"

        feel_widget = tk.Label(frame, text=feel, bg="gray")
        feel_widget.pack(side=tk.TOP, fill=tk.X)
            
        txt = self.weather.get_current_conditions()
        txt = "Today will be: " + txt
        
        # weather_widget = tk.Text(frame, bg="gray", height=2, highlightthickness=0)
        # weather_widget.insert(tk.INSERT, txt)

        weather_widget = tk.Label(frame, text=txt, bg="gray")
        
        weather_widget.pack(side=tk.TOP, fill=tk.X)
        weather = weather_widget
        
    def create_kid(self, frame, kids, kid_name, color):
        name_font_size = 34
        act_font_size = 24
        kid_name_widget = tk.Label(frame, text=kid_name, bg=color, font=("Courier", name_font_size))
        kid_name_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        school = self.schedule.get_weekly_school(kid_name)
        kid_school_widget = tk.Label(frame, text=school, bg=color, font=("Courier", act_font_size))
        kid_school_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        activity = self.schedule.get_weekly_activity(kid_name)
        kid_activity_widget = tk.Label(frame, text=activity, bg=color, font=("Courier", act_font_size))
        kid_activity_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update(self):
        cur_temp = self.weather.get_current_temp()
        high_temp = self.weather.get_high_temp()
        self.l_thermometer.update(cur_temp, high_temp)
        #self.weather.update()

if __name__ == "__main__":
    root = Root()
    root.mainloop()
