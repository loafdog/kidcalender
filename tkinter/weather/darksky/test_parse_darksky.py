import json
import os
import datetime as dt

path = os.path.dirname(os.path.abspath(__file__))
forecast_filename = path + os.path.sep + 'forecast.json'
with open(forecast_filename, 'r') as f:
    data = json.load(f)

print("cur  {} {}".format(dt.datetime.utcfromtimestamp(int(data['currently']['time'])).strftime('%Y-%m-%d %H:%M:%S'),
                         int(data['currently']['temperature'])))

# for d in data['hourly']['data']:
#     print("hour {} {}".format(dt.datetime.utcfromtimestamp(int(d['time'])).strftime('%Y-%m-%d %H:%M:%S'),
#                               int(d['temperature'])))

#now = dt.datetime.now()
now = dt.datetime.utcfromtimestamp(int(data['currently']['time']))

tomorrow = (now + dt.timedelta(hours=24)).date()

print("now      {}".format(now.date()))
print("tomorrow {}".format(tomorrow))
for d in data['daily']['data']:
    print(" day {} {} {}".format(dt.datetime.utcfromtimestamp(int(d['time'])).strftime('%Y-%m-%d %H:%M:%S'),
                                 int(d['temperatureMax']),
                                 int(d['temperatureHigh']),
                                 d['summary']))
    fcast = dt.datetime.utcfromtimestamp(d['time']).date()
    if fcast > now.date() and fcast <= tomorrow:
        print("  within 24hrs")

