#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 17:27:31 2020

@author: WS
"""

print(bleh)

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
 
users = pd.DataFrame(user_data, columns= ['First name','Last name','Initials','Username','Password','GPX'])

firsts = users['First name'].tolist()
lasts = users['Last name'].tolist()
initials = users['Initials'].tolist()
usernames = users['Username'].tolist()
passwords = users['Password'].tolist()
gpx_statii = users['GPX'].tolist()
gpx_status = gpx_statii[0]

if gpx_status == 'Y':
    
    exec(open('gpxupdate.py').read())#import does not work
    
import analyse

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
    
    if gpx_statii[user] == 'Y':
        df = pd.DataFrame(columns= ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k'])
    else:
        df = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time'])    
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
                
            if gpx_statii[user] == 'Y':
            
                print('Reading activity GPX')
                gpx_df = analyse.pull_gpx(row[0])
            
                r_times = analyse.best_times_running(gpx_df)
                #[one_k, one_m, one_five, thr_m, fiv_k, ten_k, twe_k, half, full]
                c_times = analyse.best_times_cycling(gpx_df)
                #[ten_k, twe_k, fif_k, hun_k, t_h_k, t_f_k]
            
                if row[1] != 'Running' or row[1] != 'Cycling':
                    new_row = [row[0],row[1],row[2],row[3],row[4],'N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A']
                else:
                    print('Reading activity GPX')
                    gpx_df = analyse.pull_gpx(row[0])
            
                    if row[1] == 'Running':
                        r_times = analyse.best_times_running(gpx_df)
                    else:
                        r_times = ['N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A','N/A']
                        #[one_k, one_m, one_five, thr_m, fiv_k, ten_k, twe_k, half, full]
                    if row[1] == 'Cycling':
                        c_times = analyse.best_times_cycling(gpx_df)
                    else:
                        c_times = ['N/A','N/A','N/A','N/A','N/A','N/A']
                        #[ten_k, twe_k, fif_k, hun_k, t_h_k, t_f_k]
                    new_row = [row[0],row[1],row[2],row[3],row[4],r_times[0],r_times[1],r_times[2],r_times[3],r_times[4],r_times[5],r_times[6],r_times[7],r_times[8],c_times[0],c_times[1],c_times[2],c_times[3],c_times[4],c_times[5]]
            else:
                new_row = row 
            
            a_row = pd.Series(new_row,index=df.columns)
            mod_df = df.append(a_row,ignore_index = True)
            df = mod_df.sort_values(by='Date')
            i += 1
        else:
            stop = 1
            
    df.to_csv(r'{}'.format(file_name),index=False)
    
    if stop == 1:
        print('{} activities added for {} {}'.format(i,firsts[user],lasts[user]))
   
print('Update complete!')
        
    
