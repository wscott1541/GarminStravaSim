#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:56:05 2020

@author: WS
"""

import time
from datetime import datetime

#sort activity into vaguely useable forms
def pull_from_activity(activity):
    string_activity = str(activity)

    string_activity = string_activity.replace('[{','')
    string_activity = string_activity.replace('}]','')

    list_activity_strings = string_activity.split(',')

    #pull useful information (date, type, duration, distance)

    date_string = list_activity_strings[3][20:-1]
    type_string = list_activity_strings[6][13:-1]    
    type_string = type_string.capitalize()
    if type_string == 'Indoor_cardio':
        type_string = 'Cardio'
    durs_string = list_activity_strings[16][20:]#16 is elapsed duration (ms), 15 is duration (s)
    dist_string = list_activity_strings[14][13:]
    dist_float = round(float(dist_string)/1000,2)#convert from m to km
    dist_string = str(dist_float)

    durs_float = float(durs_string)/1000#convert from milliseconds to seconds
    durs_string = time.strftime('%H:%M:%S',time.gmtime(durs_float))

    row = [type_string,date_string,dist_string,durs_string]
    
    return(row)

#requires garminconnect, and all pulled from - https://pypi.org/project/garminconnect/
from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

username = input('Username: ')
password = input('Password: ')

#could add login if command
try:
    client = Garmin(username, password)
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occured during Garmin Connect Client init: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occured during Garmin Connect Client init")
    quit()

try:
    client.login()
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occured during Garmin Connect Client login: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occured during Garmin Connect Client login")
    quit()

import pandas as pd

data = pd.read_csv (r'Activities.csv')   
df = pd.DataFrame(data, columns= ['Activity Type','Date','Distance','Time'])
#add an archive function?
df = df.sort_values(by='Date')

#check the most recent date
dates_list = df['Date'].tolist()
latest_date = dates_list[-1]
latest_date_strp = datetime.strptime(latest_date,'%Y-%m-%d %H:%M:%S')
latest_date_object = datetime.timestamp(latest_date_strp)

stop = 0
i = 0
while stop == 0:
    try:
        pulled_activity = client.get_activities(i,i + 1) # 0=start, 1=limit
        #could work out how to do several of these at once, limiting number of requests
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        print("Error occured during Garmin Connect Client get activities: %s" % err)
        quit()
    except Exception:  # pylint: disable=broad-except
        print("Unknown error occured during Garmin Connect Client get activities")
        quit()
        
    row = pull_from_activity(pulled_activity)# row = [type_string,date_string,dist_string,durs_string]
    
    row_date_string = row[1]
    row_date_strp = datetime.strptime(row_date_string,'%Y-%m-%d %H:%M:%S')
    row_date_object = datetime.timestamp(row_date_strp)
    
    if row_date_object > latest_date_object:
        a_row = pd.Series(row,index=df.columns)
        mod_df = df.append(a_row,ignore_index = True)
        df = mod_df.sort_values(by='Date')
        i += 1
    else:
        stop = 1

df.to_csv(r'Activities.csv', index = False)
if stop == 1:
    print('Import complete')