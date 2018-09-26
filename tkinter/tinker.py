import tkinter as tk

from datetime import date
import calendar
import json
import requests
import os
import pdb
import schedule

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.schedule = schedule.Schedule()

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
        weather_text.insert(tk.INSERT, "Cloudy")
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
        d = None
        try:
            d = self.read_forecast()
        except:
            d = self.forecast_api()
            self.write_forecast(d)

        c = None
        try:
            c = self.read_conditions()
        except:
            c = self.conditions_api()
            self.write_conditions(c)

        #pdb.set_trace()
        
        cur_temp = int(c['current_observation']['temp_f'])
        print("current_temp: %s" % cur_temp)

        self.draw_temp_bar(cur_temp, self.l_thermometer, 100, self.height, "current_temp_bar")

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

if __name__ == "__main__":
    root = Root()
    root.mainloop()
