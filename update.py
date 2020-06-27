#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 17:27:31 2020

@author: WS
"""

import pandas as pd

from time import time

from datetime import datetime

today = time()

today_dt = datetime.fromtimestamp(today)
today_string = datetime.strftime(today_dt,'%Y-%m-%d')

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

from pull_activity import pull_from_activity

#Pull user details
user_data = pd.read_csv (r'users.csv')  
 
users = pd.DataFrame(user_data, columns= ['First name','Last name','Initials','Username','Password'])

firsts = users['First name'].tolist()
lasts = users['Last name'].tolist()
initials = users['Initials'].tolist()
usernames = users['Username'].tolist()
passwords = users['Password'].tolist()

#pull activities
for user in range(0,len(initials)):
    
    #log into Garmin
    try:
        client = Garmin(usernames[user], passwords[user])
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
        
    file_name = "{}activities.csv".format(initials[user])
    
    data = pd.read_csv(r'{}'.format(file_name))
    
    df = pd.DataFrame(data, columns= ['Activity Type','Date','Distance','Time'])
    df = df.sort_values(by='Date')

    #check the most recent activity date
    dates_list = df['Date'].tolist()
    latest_date = dates_list[-1]
    latest_date_strp = datetime.strptime(latest_date,'%Y-%m-%d %H:%M:%S')
    latest_date_object = datetime.timestamp(latest_date_strp)
    
    #addd activities since last updated
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
            quit()
        except Exception:  # pylint: disable=broad-except
            print("Unknown error occured during Garmin Connect Client get activities")
            quit()
        
        row = pull_from_activity(pulled_activity)# row = [type_string,date_string,dist_string,durs_string]
    
        row_date_string = row[1]
        row_date_strp = datetime.strptime(row_date_string,'%Y-%m-%d %H:%M:%S')
        row_date_object = datetime.timestamp(row_date_strp)
    
        if row_date_object > latest_date_object:
            if i == 0:
                #archive only if update necessary
                archive = pd.DataFrame(data)
                archive.to_csv(r'{}{}'.format(today_string,file_name), index = False)
        
            a_row = pd.Series(row,index=df.columns)
            mod_df = df.append(a_row,ignore_index = True)
            df = mod_df.sort_values(by='Date')
            i += 1
        else:
            stop = 1
            
    df.to_csv(r'{}'.format(file_name),index=False)
    
    if stop == 1:
        print('{} activities added for {} {}'.format(i,firsts[user],lasts[user]))
   
print('Update complete!')
        
    
