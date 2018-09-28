import tkinter as tk

from datetime import date
import calendar
import json
import requests
import os
import pdb
import schedule
import weather

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.schedule = schedule.Schedule()
        self.weather = weather.Forecast()

        self.width = 800
        self.height = 400
        
        self.title("Thermometer")
        self.geometry("{}x{}".format(self.width,self.height))


        self.l_thermometer_frame = tk.Frame(self)
        self.l_thermometer = self.create_thermometer(self.l_thermometer_frame, 100, self.height)

        self.r_thermometer_frame = tk.Frame(self)
        self.r_thermometer = self.create_thermometer(self.r_thermometer_frame, 100, self.height)

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

        self.l_thermometer_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.r_thermometer_frame.pack(side=tk.RIGHT, fill=tk.Y)
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

    def create_date(self, frame):
        date_str = self.schedule.get_date_str()
        day_str = self.schedule.get_day_str()

        date_widget = tk.Label(frame, text=date_str, bg="gray")
        date_widget.pack(side=tk.TOP, fill=tk.X)
        
        day_widget = tk.Label(frame, text=day_str, bg="gray")
        day_widget.pack(side=tk.TOP, fill=tk.X)
        

    def create_weather(self, frame, weather):
        weather_text = tk.Text(frame, bg="gray", height=2, highlightthickness=0)
        txt = self.weather.get_current_conditions()
        weather_text.insert(tk.INSERT, txt)
        weather_text.pack(side=tk.TOP, fill=tk.X)
        weather = weather_text
        
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


    def old_create_kid(self, frame, kids, kid_name, color):
        kid_name_widget = tk.Label(frame, text=kid_name, bg=color)
        kid_name_widget.pack(side=tk.TOP, fill=tk.X)

        kid_activity_widget = tk.Text(frame, bg=color, height=5, highlightthickness=0)
        school = self.schedule.get_weekly_school(kid_name)
        act = self.schedule.get_weekly_activity(kid_name)
        print(school, act)
        kid_activity_widget.insert(tk.INSERT, school + "\n")
        kid_activity_widget.insert(tk.INSERT, act)
        #kid_activity_widget.insert(tk.INSERT, "Gym")
        kid_activity_widget.pack(side=tk.TOP, fill=tk.X)
        kids[kid_name] = kid_activity_widget

    def create_thermometer(self, frame, w, h):
        t = tk.Canvas(frame, width=w, height=h, highlightthickness=0)
        t.pack(side=tk.TOP)

        temp_colors = {
            100 : "red",
            90 : "red",
            80 : "orange",
            70 : "orange",
            60 : "yellow",
            50 : "yellow",
            40 : "green",
            30 : "green",
            20 : "cyan",
            10 : "cyan",

        }

        rw = w
        rh = h/len(temp_colors)
        for i in range(0, len(temp_colors)):
            temp = 100-(i*10)
            t.create_rectangle(0,i*rh,rw,(i*rh)+rh,fill=temp_colors[temp])
            t.create_text(10, i*rh-7, text=str(temp))

        self.draw_temp_bar(10, t, w, h, "current_temp_bar")

        return t

    def draw_temp_bar(self, temp, thermometer, w, h, name):
        # scale temp to graphic range: 0-100 -> 0-h  temp/100*h 
        th = (100-temp)/100*h
        text = str(temp) + ""
        thermometer.delete(name)
        thermometer.create_rectangle(w/2,th,w/2+5,h,fill="black", tags=name)
        thermometer.create_text(w/2,th-10, text=text, tags=name)
        
    def update(self):
        cur_temp = self.weather.get_current_temp()
        self.draw_temp_bar(cur_temp, self.l_thermometer, 100, self.height, "current_temp_bar")
        #self.weather.update()

if __name__ == "__main__":
    root = Root()
    root.mainloop()
