
# coding: utf-8

# In[ ]:

import requests
import json
import databaseconnect as dbc
import pandas as pd

#create function to call weather underground API and process dates correctly
def get_change_data(year):
    url = 'http://www.wunderground.com/history/airport/KDCA/%s/1/1/CustomHistory.html?dayend=31&monthend=12&yearend=%s&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=&format=1'
    data = pd.read_csv(url % (year,year),sep=',')
    df = pd.DataFrame(data['EST'].str.split('-',2).tolist(),
                                   columns = ['year','month','day'])

    df['month'] = df['month'].str.zfill(2)
    df['day'] = df['day'].str.zfill(2)
    df['date'] = df['year']+'-'+df['month']+'-'+df['day']

    data['date'] =  df['date']
    data['date'] = pd.to_datetime(data['date'], format = '%Y-%M-%d')
    return(data)

#loop through past 5 years of data
years = [2012,2013,2014,2015,2016]
for year in years:
    ## This is the first year, so create a df of this
    if year == 2012:
        weather = get_change_data(year)
    else:
        ## otherwise append rest of data
        weather = pd.concat([weather,get_change_data(year)])

#call engine
eng = dbc.get_engine('server_info.yml', 'database1')

#copy data to db
weather.to_sql('weather_database',eng,if_exists="replace")

