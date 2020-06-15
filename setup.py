#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 12:46:12 2020

@author: WS
"""

import pandas as pd

username = input('Username: ')
password = input('Password: ')

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

"""Log into Garmin"""
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
    
"""Fetch name"""

try:
    full_name = client.get_full_name()
except (
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
) as err:
    print("Error occured during Garmin Connect Client get full name: %s" % err)
    quit()
except Exception:  # pylint: disable=broad-except
    print("Unknown error occured during Garmin Connect Client get full name")
    quit()

split_name = full_name.split()
first_name = split_name[0]
last_name = split_name[-1]
first_initial = first_name[0]
last_initial = last_name[0]
initials = '{}{}'.format(first_initial,last_initial)

"""Write details to csv file to store"""

titles = pd.DataFrame(columns= ['First name','Last name','Initials','Username','Password'])

user_details = [first_name,last_name,initials,username,password]
user_row = pd.Series(user_details,index=titles.columns)
users = titles.append(user_row,ignore_index = True)

users.to_csv(r'users.csv',index = False)

"""Create file with actitivies, tied to user initials"""

from pull_activity import pull_from_activity

df = pd.DataFrame(columns= ['Activity Type','Date','Distance','Time'])

import_error = 0
stop = 0
i = 0
while stop == 0:
    try:
        pulled_activity = client.get_activities(i,i + 1) # 0=start, 1=limit
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        print("Error occured during Garmin Connect Client get activities: %s" % err)
        stop = 1
        import_error = 1
    except Exception:  # pylint: disable=broad-except
        print("Unknown error occured during Garmin Connect Client get activities")
        stop = 1
        import_error = 1
    
    if len(pulled_activity) > 0:
        row = pull_from_activity(pulled_activity)
        print('Importing activity',i + 1)
        a_row = pd.Series(row,index=df.columns)
        mod_df = df.append(a_row,ignore_index = True)
        df = mod_df.sort_values(by='Date')
        
        i += 1
    else:
        stop = 1

file_name = "{}activities.csv".format(initials)

df.to_csv(r'{}'.format(file_name),index=False)

if stop == 1 and import_error == 0:
    print('Import complete - {} activities!'.format(i))