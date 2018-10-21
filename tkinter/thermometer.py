import tkinter as tk

class Thermometer():

    def __init__(self, frame, width, height, name):
        self.height = height
        self.width = width
        self.name = name
        self.frame = tk.Frame(frame)
        #self.thermometer = self.create_thermometer(self.thermometer_frame, width, height)
        self.thermometer = self.create()

    def create(self):
        t = tk.Canvas(self.frame, width=self.width, height=self.height, highlightthickness=0)
        t.pack(side=tk.TOP)

        temp_colors = {
            100 : "orange",
            90 : "orange",
            80 : "yellow",
            70 : "yellow",
            60 : "green",
            50 : "green",
            40 : "cyan",
            30 : "cyan",
            20 : "purple",
            10 : "purple",
        }
        # temp_colors = {
        #     100 : "red",
        #     90 : "red",
        #     80 : "orange",
        #     70 : "orange",
        #     60 : "yellow",
        #     50 : "yellow",
        #     40 : "green",
        #     30 : "green",
        #     20 : "cyan",
        #     10 : "cyan",

        # }

        rw = self.width
        rh = self.height/len(temp_colors)
        for i in range(0, len(temp_colors)):
            temp = 100-(i*10)
            t.create_rectangle(0,i*rh,rw,(i*rh)+rh,fill=temp_colors[temp])
            t.create_text(10, i*rh-7, text=str(temp))

        #self.draw_temp_bar(10, t, self.width, self.height, "current_temp_bar")
        #self.draw_temp_bar(10)

        return t

    def draw_current_temp(self, temp):
        # scale temp to graphic range: 0-100 -> 0-h  temp/100*h
        x1 = self.width/2
        y1 = (100-temp)/100*self.height
        x2 = self.width/2+5
        y2 = self.height

        # text
        # tx = self.width/2
        # ty = y1-10
        tx = x2 - 20
        ty = y1 + 10
        
        text = str(temp)
        self.thermometer.delete(self.name)
        self.thermometer.create_rectangle(x1,y1,x2,y2,fill="black", tags=self.name)
        self.thermometer.create_text(tx,ty, text=text, tags=self.name)

    def draw_high_temp(self, temp):
        x1 = self.width/2 + 10
        y1 = (100-temp)/100*self.height + 5
        x2 = self.width
        y2 = y1-5

        # text
        tx = self.width*.75 - 5
        ty = y1-20
        
        text = "HIGH\n" + str(temp)
        self.thermometer.delete(self.name + 'h')
        self.thermometer.create_rectangle(x1,y1,x2,y2,fill="black", tags=self.name + 'h')
        self.thermometer.create_text(tx,ty, text=text, tags=self.name + 'h')
        
    def update(self, temp, high):
        self.draw_current_temp(temp)
        self.draw_high_temp(high)
