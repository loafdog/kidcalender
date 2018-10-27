# kidcalender
Mom, Dad, is it gonna be hot or cold, what should I wear, do i have gym today?

Tired of your kids asking you what's the weather, what should I wear?
Or maybe they get up in the morning in middle of winter on a 32 degree
day and come to breakfast wearing a t-shirt and shorts.  This aims to
solve the problem by over-engineering as much as possible.

# Running the app
python3 is required.

To run the app all you need to do is move to tkinter dir and run:
`python tinker.py`

It runs on desktop/laptop or a raspberry pi.

# App versions
There are multiple versions of same/similar project in this repo. I
wanted to try out different gui frameworks.

## tkinter
This is the second version of the app.  It uses tkinter and python.
Tkinter is a Python binding to the Tk GUI toolkit. You should not have
to install any extra python or GUI pkgs to get app to run.

You can run the app without configuring anything.  There is a
sample_config and sample_schedule that allow the app to run w/o you
configuring anything.  In the weather module there are sample api
responses from the weather forecast apis used.

## pygame
First version uses pygame and python.  Runs on laptop or a raspberry
pi with 7" touch screen.  It was a fun/good learning experience but in
the end I'm not too happy with it. Really hard to maintain and
remember what I did.  App also started to freeze after running for a
few days/weeks on the raspberry pi.  There are no config files
available so if you try to use this version you'll have to figure out
what code to edit to make it run.  I have given up on this
version so I consider it dead code.

## Weather Forecast APIs
To get weather forecast and current condition the app makes api calls
to a weather service. So you will need an internet connection and an
API key to use this app.

### darksky
Go here to sign up for an API key: https://darksky.net/dev

Copy the sample_config.json to file located/called
kidcalendar/tkinter/config.json

Here's a snippet from config.json that shows what needs to be edited.

```
    "darksky": {
        "api_key": "your api key",
        "lat_long": "lat,long"
    }
```
The api_key value is what you get by signing up with darksky.

I determined the lat,long values by going to google map and selecting
a location near me.

### wunderground
For the first attempt I chose to use api.wunderground.com to get
weather info.  Since I started this project I guess the free service
has been ended. See http://api.wunderground.com/weather/api If you
still wish to use this api you are on your own to figure out how to
get/pay for an API key.  I did not remove support for this api so you
can still use it.

Copy the sample_config.json to file located/called
kidcalendar/tkinter/config.json

To use wunderground you need to edit following section of config.json

```
    "wunderground": {
        "api_key":"your api key",
        "state":"your state",
        "city":"your city"
    },
```
You also will need to edit tinker.py here: https://github.com/loafdog/kidcalender/blob/master/tkinter/tinker.py#L21
Comment out darksky import and uncomment wunderground import.


### openweathermap
I looked briefly at https://openweathermap.org/ Tried out the api and
browsed around their site.  Meh.. something just rubbed me the wrong
way about it.
