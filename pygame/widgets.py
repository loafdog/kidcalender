import pygame, sys
#from pygame.locals import *

class Colors:
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    RED   = (255, 50, 50)
    ORANGE = (255, 150, 50)
    YELLOW = (255, 255, 0)
    GREEN = (50, 255, 50)
    CYAN = (0, 255, 255)
    BLUE  = (50, 50, 255)
    PINK = (255, 105, 180)
    PURPLE = (155, 48, 255)

class Thermometer:
    """Display Thermometer
    Handle clicks on thermometer
    """

    temp_colors = {
        100 : Colors.RED,
        90 : Colors.RED,
        80 : Colors.ORANGE,
        70 : Colors.ORANGE,
        60 : Colors.YELLOW,
        50 : Colors.YELLOW,
        40 : Colors.GREEN,
        30 : Colors.GREEN,
        20 : Colors.CYAN,
        10 : Colors.CYAN,
        0 : Colors.CYAN
    }

    def __init__(self, scr, scr_w, scr_h, t_x, t_y, t_w, t_h, temp_val, therm_str ):
        self.scr = scr
        self.scr_w = scr_w
        self.scr_h = scr_h

        if t_y == -1:
            self.t_y = 25
        else:
            self.t_y = t_y
        if t_w == -1:
            self.t_w = 75
        else:
            self.t_w = t_w
        if t_h == -1:
            # make it a tad smaller than height of screen
            self.t_h = scr_h - 100
        else:
            self.t_h = t_h
        if t_x == -1:
            # divide screen in half and put therm at offset of self.t_w/2
            self.t_x = (scr_w/2) - (self.t_w/2)
        else:
            self.t_x = t_x
            
        self.temp_val = temp_val
        self.therm_str = therm_str

        self.t_line_width = 5

        self.myfont = pygame.font.SysFont("monospace", 20)


    def update_temp(self, temp_val):
        self.temp_val = int(temp_val)
        
    def is_inbounds(self, x, y):
        """Check if given x,y is in bounds of thermometer
        """
        return self.t_x < x < self.t_x + self.t_w and \
               self.t_y < y < self.scr_h
    
    def draw(self):
        # draw outline of thermometer
        self.t_outline_rect = [self.t_x, self.t_y, self.t_w, self.t_h]
        pygame.draw.rect(self.scr, Colors.BLACK, self.t_outline_rect, self.t_line_width)
        print("self.t_outline_rect %s" % self.t_outline_rect)

        # Show label and temp below thermometer
        temp_label_font = pygame.font.SysFont("monospace", 20)
        therm_label_str = str(self.therm_str)
        therm_label = self.myfont.render(therm_label_str, 1, Colors.BLACK)
        therm_label_points = (self.t_x, self.t_y + self.t_h)
        self.scr.blit(therm_label, therm_label_points)
        temp_label_font = pygame.font.SysFont("monospace", 40)
        therm_label_str = str(self.temp_val)
        therm_label = temp_label_font.render(therm_label_str, 1, Colors.BLACK)
        therm_label_points = (self.t_x, self.t_y + self.t_h + 20)
        self.scr.blit(therm_label, therm_label_points)


        total_h = self.t_h - (self.t_line_width * 2)
        print("total_h", total_h)
        
        tick_interval = int(total_h/10)
        print("tick_interval ", tick_interval)

        # Adjust therm_y to move ticks up/down and color boxes up down.
        # If the position of the first and last box don't line up with top
        # and bottom of therm outline box.. then need to add if stmt in
        # loop to change the y pos and height of the first and last color
        # box to fill up the gaps.
        #
        # Too far up
        # therm_y = self.t_y
        # Too far down
        # therm_y = self.t_y + self.t_line_width
        #
        # Just right. This causes tick marks to be right at top of the
        # therm box. may make it hard to read.
        therm_y = self.t_y + (self.t_line_width/2)
        therm_x = self.t_x
        
        # start at 100 and count down
        temp = 100
        
        # This isn't working.. i think that the space between top and
        # bottom rects in therm are just different because of thickness of
        # therm lines.  Need to handle the first and last rect
        # separately. The rest can be drawn in a loop.
        # for i in range(self.t_y, self.t_h-tick_interval, tick_interval):
        # for i in range(self.t_y, self.t_h, tick_interval):
        for i in range(0,10):
            
            if temp in Thermometer.temp_colors:
                temp_color = Thermometer.temp_colors[temp]
            else:
                temp_color = Colors.WHITE

            # calc temp tick line
            tick_x = therm_x
            tick_y = therm_y + (i * tick_interval)
            
            # Draw a box between tick marks to be filled in with a color
            # rect is x,y,w,h
            temp_box_x = tick_x+self.t_line_width-2
            temp_box_y = tick_y
            temp_box_w = self.t_w-self.t_line_width-1
            temp_box_h = tick_interval
            # If there is a gap at the top, use this to fix that.
            # if i == 0:
            #     temp_box_y=self.t_y+(self.t_line_width/2)
            #     temp_box_h+=5
            if i == 9:
                #temp_box_y=self.t_y+(self.t_line_width/2)
                temp_box_h+=5

            temp_color_box = [temp_box_x, temp_box_y, temp_box_w, temp_box_h]
            #temp_color_box = [self.t_x+self.t_line_width-2, self.t_y+i, self.t_w-self.t_line_width-1, tick_interval]
            #temp_color_box = [self.t_x+self.t_line_width-2, self.t_y+i+self.t_line_width+2-tick_interval, self.t_w-self.t_line_width-1, tick_interval+5]
            #print("temp_color %s" % temp_color_box)
            pygame.draw.rect(self.scr, temp_color, temp_color_box, 0)

            # draw temp tick line
            points = [(tick_x, tick_y),(tick_x+10, tick_y)]
            #print("temp line: %s" % points)
            pygame.draw.lines(self.scr, Colors.BLACK, False, points, 4)

            # Draw temp number near tick mark
            temp_label = self.myfont.render(str(temp), 1, Colors.BLACK)
            temp_label_points = (tick_x+15, tick_y)
            #print("temp_label_points %s" % str(temp_label_points))
            self.scr.blit(temp_label, temp_label_points)
            temp-=10

        # Draw rectangle to show current temp. map self.temp_val to y of top of
        # rect.
        #
        # scale temp to graphic range: 0-100 -> 10->400  x/100*400 self.temp_val/100*self.t_h
        #
        # then shift to bottom of temp rectangle
        fudge = self.t_line_width - 1
        cur_h = (self.temp_val / 100) * (self.t_h - self.t_line_width) + fudge
        
        #cur_y = self.t_y + self.t_line_width +((100 - self.temp_val) / 100 * self.t_h)
        #cur_y = self.t_y + ((100 - self.temp_val) / 100 * self.t_h)
        
        cur_y = self.t_y + ((100 - self.temp_val) / 100 * self.t_h) - fudge
        cur_x = self.t_x + self.t_w - 20
        
        
        cur_w = 10
        self.temp_val_rect = [cur_x,cur_y,cur_w,cur_h]
        print("self.temp_val %s" % self.temp_val)
        print("self.temp_val_rect %s" % self.temp_val_rect)
        pygame.draw.rect(self.scr, Colors.BLACK,self.temp_val_rect, 0)
    
class NameInfo:
    """Display info about each kid
    """

    def __init__(self, scr, scr_w, scr_h, x, y, temp_val, kid, schedule):
        self.scr = scr
        self.scr_w = scr_w
        self.scr_h = scr_h
        self.x = x
        self.y = y
        self.temp_val = temp_val
        self.kid = kid
        self.schedule = schedule

        # def display_name_info(scr, scr_w, scr_h, x, y, cur_temp, kid):

    def draw(self):
        lines = []
        lines.extend(self.schedule.get_activity(self.kid))
        lines.extend(self.schedule.get_what_to_wear(self.kid, self.temp_val))
        print("LINES",lines)
        
        name_font_size = 50
        font_size = 25
        line_space = 10
        # This is how much space the date line takes.  Maybe should pass
        # it into this function. Or make this whole thing a class!
        date_offset = 70
        
        line_font = pygame.font.SysFont("monospace", font_size)
        name_font = pygame.font.SysFont("monospace", name_font_size)
        
        name_label = name_font.render(self.kid.title(), 1, Colors.BLACK)
        labels = []
        for line in lines:
            if line == None:
                continue
            #print("LINE: ", line)
            labels.append(line_font.render(line, 1, Colors.BLACK))
            
        self.scr.blit(name_label, (self.x, self.y + date_offset))        
        for line in range(len(labels)):
            self.scr.blit(labels[line],(self.x, self.y + name_font_size + date_offset + (line*font_size+(line_space*line))))
                
class DayInfo:
    """Display day info
    """

    def __init__(self, scr, scr_w, scr_h, x, y, schedule):
        self.scr = scr
        self.scr_w = scr_w
        self.scr_h = scr_h
        self.x = x
        self.y = y
        self.schedule = schedule

    def draw(self):
        label_day_str,label_date_str = self.schedule.get_day_info()
        myfont = pygame.font.SysFont("monospace", 40)

        single_line = True
        if single_line:
            label_date = myfont.render(label_day_str + " " + label_date_str, 1, Colors.BLACK)
            self.scr.blit(label_date, (self.x+5, self.y+25))
        else:
            label_day = myfont.render(label_day_str, 1, Colors.BLACK)
            label_date = myfont.render(label_date_str, 1, Colors.BLACK)

            self.scr.blit(label_day, (self.x+50, self.y+15))
            self.scr.blit(label_date, (self.x+(self.scr_w/2)-40, self.y+15))


