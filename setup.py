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

gpx_status = input('Would you like to import gpx files for analysis? (Y/N) ')

"""Write details to csv file to store"""

titles = pd.DataFrame(columns= ['First name','Last name','Initials','Username','Password','GPX'])

user_details = [first_name,last_name,initials,username,password,gpx_status]
user_row = pd.Series(user_details,index=titles.columns)
users = titles.append(user_row,ignore_index = True)

users.to_csv(r'users.csv',index = False)

"""Get GPX files"""

#if gpx_status == 'Y':
    
    #exec(open('gpxsetup.py').read())#import does not work

"""Create file with actitivies, tied to user initials"""

from pull_activity import pull_from_activity

if gpx_status == 'Y':
    df = pd.DataFrame(columns= ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k'])
else:
    df = pd.DataFrame(columns= ['Activity number','Activity Type','Date','Distance','Time'])

import analyse

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
        """
        if gpx_status == 'Y':
            
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
        """
        a_row = pd.Series(row,index=df.columns)
        mod_df = df.append(a_row,ignore_index = True)
        df = mod_df.sort_values(by='Date')
        
        print('Imported!')
        
        i += 1
    else:
        stop = 1

file_name = "{}activities.csv".format(initials)

df.to_csv(r'{}'.format(file_name),index=False)

if stop == 1 and import_error == 0:
    print('Import complete - {} activities!'.format(i))