from __future__ import division

import pygame, sys
from pygame.locals import *

import weather
import screen_saver
import schedule
import widgets

forecast_obj = weather.Forecast()

schedule_obj = schedule.Schedule()

def display_names_info(scr, scr_w, scr_h, x, y, cur_temp):
    name_x = x + 20
    #display_name_info(scr, scr_w, scr_h, name_x, y, cur_temp, "greta")
    g_info = widgets.NameInfo(scr, scr_w, scr_h, name_x, y, cur_temp, "greta", schedule_obj)

    name_x = scr_w/2 + 20
    #display_name_info(scr, scr_w, scr_h, name_x, y, cur_temp, "cora")
    c_info = widgets.NameInfo(scr, scr_w, scr_h, name_x, y, cur_temp, "cora", schedule_obj)

    g_info.draw()
    c_info.draw()
    

def update_display(scr, scr_w, scr_h, thermometer_current, thermometer_forecast):

    # check if schedule changed or fcast changed else do nothing

    #scr.fill(WHITE)

    scr.fill(widgets.Colors.PINK)
    #scr.fill(PURPLE)
    pygame.draw.rect(scr, widgets.Colors.PURPLE, [0,0,scr_w/2,scr_h], 0)

    
    thermometer_current.update_temp(forecast_obj.current_temp())
    thermometer_forecast.update_temp(forecast_obj.forecast_temp())
        
    thermometer_current.draw()
    thermometer_forecast.draw()
    
    x = 75
    y = -1
    #display_day_info(scr, scr_w-150, scr_h, x, y)
    day_info = widgets.DayInfo(scr, scr_w-150, scr_h, x, y, schedule_obj)
    day_info.draw()
    # names(scr, scr_w, scr_h-150, x, y, forecast_temp)
    #what_to_wear(scr, scr_w, scr_h, x, y, forecast_temp)
    display_names_info(scr, scr_w, scr_h, x, y, forecast_temp)
    
        
#############################################################################
# MAIN
#############################################################################


pygame.init()
#scr = pygame.display.set_mode((400, 300))
# size of 7" pi tft
#scr = pygame.display.set_mode((800, 480))

scr_w=790
scr_h=390

# fits well when running in desktop
scr = pygame.display.set_mode((scr_w, scr_h))
#scr = pygame.display.set_mode((scr_w, scr_h), FULLSCREEN)

################################################################################

scr.fill(widgets.Colors.PINK)
#scr.fill(PURPLE)
pygame.draw.rect(scr, widgets.Colors.PURPLE, [0,0,scr_w/2,scr_h], 0)
pygame.display.set_caption('Greta&Cora Weather Calendar')

current_temp=forecast_obj.current_temp()
current_therm_x = 1
current_therm_y = 25
current_therm_w = 75
current_therm_h = -1
thermometer_current =\
    widgets.Thermometer(scr, scr_w, scr_h,
                            current_therm_x, current_therm_y,
                            current_therm_w, current_therm_h,
                            current_temp, 'Current')

forecast_temp = forecast_obj.forecast_temp()
#forecast_temp=40
forecast_therm_w = 75
forecast_therm_h = -1
forecast_therm_x = (scr_w - forecast_therm_w - 1)
forecast_therm_y = 25
thermometer_forecast = \
    widgets.Thermometer(scr, scr_w, scr_h,
                            forecast_therm_x, forecast_therm_y,
                            forecast_therm_w, forecast_therm_h,
                            forecast_temp, 'High')

update_display(scr, scr_w, scr_h, thermometer_current, thermometer_forecast)


forecast_obj.start_update_timer()

run_main = True
try:
    # TODO get screen saver time from conf file
    screen_saver = screen_saver.BlankScreen()
    screen_saver.start_timer()
    
    while run_main: # main game loop

        # need to redraw display.. so we can see date change, forecast
        # change, schedule change. Need fast way to check if anything
        # changed. maybe there is a way to slow this loop down?
        #
        #update_display(scr, scr_w, scr_h, thermometer_current, thermometer_forecast)
        event = pygame.event.wait()
        if event != None:
            
            screen_saver.reset_timer()
            
            if event.type == QUIT:
                run_main = False
                
            elif(event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                print("DOWN: ",pos)
                x,y = pos

                screen_saver.off()
            
                if thermometer_current.is_inbounds(x,y):
                    print("CURRENT: SHOULD EXIT")
                    run_main = False
               
                elif thermometer_forecast.is_inbounds(x,y):
                    print("FORECAST: SHOULD REFRESH")
                    # TODO: add call to update forecast
                    forecast_obj.timed_update()
                    #forecast_obj.timed_update('s')
                    #forecast_obj.throw_except()
               
            elif(event.type is USEREVENT):
                print("USERDATA: ", event.data)
                update_display(scr, scr_w, scr_h, thermometer_current, thermometer_forecast)
        #    pygame.display.flip
        pygame.display.update()
except Exception as ex:
    print("Caught unexpected ex: ", ex)
    run_main = False

screen_saver.stop_timer()
screen_saver.off()
forecast_obj.stop_update_timer()
pygame.quit()
sys.exit()
    
