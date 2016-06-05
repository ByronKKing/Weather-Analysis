
# coding: utf-8

# In[3]:

## Import all packages

import requests
import json
import databaseconnect as dbc
import pandas as pd

## Get Ten Day Predictions

# make request to Weather Underground API
r = requests.get('http://api.wunderground.com/api/acec5ab1b5aa1eba/forecast10day/q/DC/Washington.json')

# decode the JSON response body into a dictionary
jsonObj = r.json()


# extracting the forecastday from the dictionary
forecast = jsonObj['forecast']
forecastday = forecast.get('simpleforecast').get('forecastday')


#get all desired info into empty json frame
jsonList = []
for record in forecastday:
    currentJson = {}
    currentJson['high_celsius'] = float(record.get('high').get('celsius'))
    currentJson['high_fahrenheit']  = float(record.get('high').get('fahrenheit'))
    currentJson['high_celsius']  = float(record.get('low').get('celsius'))
    currentJson['high_fahrenheit']  = float(record.get('low').get('fahrenheit'))
    currentJson['qpfday_in']  = float(record.get('qpf_day').get('in'))
    currentJson['qpfday_mm']  = float(record.get('qpf_day').get('mm'))
    currentJson['avehumidity']  = float(record.get('avehumidity'))
    currentJson['conditions']  = (record.get('conditions'))
    currentJson['date']  = (record.get('date').get('pretty'))
    currentJson['weekday']  = (record.get('date').get('weekday'))
    currentJson['month']  = (record.get('date').get('monthname'))
    jsonList.append(currentJson)


#make pandas dataframe
weather = pd.DataFrame(jsonList)


# In[4]:

#create connection with auxilary db
eng = dbc.get_engine('server_info.yml', 'database1')

#copy data to db
weather.to_sql('weather_prediction_database',eng,if_exists="replace")

