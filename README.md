# kidcalender
Mom, Dad, is it gonna be hot or cold, what should I wear, do i have gym today?

Tired of your kids asking you what's the weather, what should I wear?
Or maybe they get up in the morning in middle of winter on a 32 degree
day and come to breakfast wearing a t-shirt and shorts.  This aims to
solve the problem by over-engineering as much as possible.

First version uses pygame and python.  Runs on laptop or a raspberry
pi with 7" touch screen.  I'm not happy with it. Really hard to
maintain and remember what I did.  It also started to freeze after
running for a few days/weeks.  There are no config files available so
if you try to use this version you'll have to figure it out.  I have
given up on this version so I consider it dead code.

Second version uses tkinter and python.  Tkinter is a Python binding
to the Tk GUI toolkit. You should not have to install anything GUI
pkgs to get app to run.  There is a sample_config and sample_schedule
that allow the app to run w/o you configuring anything.

The app uses api.wunderground.com to get weather info.  Since I
started this project I guess the free service has been ended. See
http://api.wunderground.com/weather/api

So.. I need to find an alternative weather API service.
https://openweathermap.org/ looks promising.


To run the app all you need to do is move to tkinter dir and run:
`python tinker.py`

python3 is required.
