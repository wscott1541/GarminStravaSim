 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 17:27:31 2020

@author: WS
"""

#print(bleh)

import pandas as pd

from time import time

from datetime import datetime

import os

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
#gpx_status = gpx_statii[0]

#if gpx_status == 'Y':
    
#    exec(open('gpxupdate.py').read())#import does not work
    
import analyse

#pull activities
for user in range(1,len(initials)):#1 to only update WM because mine should have been updated manually anyway
    
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
        df = pd.DataFrame(columns= ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status'])
    else:
        df = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time'])    
    df = df.sort_values(by='Date')

    temp_df = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time'])

    #check the most recent activity date
    dates_list = temp_df['Date'].tolist()
    latest_date = dates_list[-1]
    latest_date_strp = datetime.strptime(latest_date,'%Y-%m-%d %H:%M:%S')
    latest_date_object = datetime.timestamp(latest_date_strp)
    
    temp_df = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time'])
    
    #add activities since last updated
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
        
        row = pull_from_activity(pulled_activity)# row = [activtity,type_string,date_string,dist_string,durs_string]
    
        row_date_string = row[2]
        row_date_strp = datetime.strptime(row_date_string,'%Y-%m-%d %H:%M:%S')
        row_date_object = datetime.timestamp(row_date_strp)
    
        if row_date_object > latest_date_object:
            if i == 0:
                #archive only if update necessary
                archive = pd.DataFrame(data)
                fileDir = os.path.dirname(os.path.realpath('__file__'))
                archname = os.path.join(fileDir, 'Archive.gitignore/{}{}.csv'.format(today_string,file_name))
                #archive = pd.DataFrame(data)
                archive.to_csv(r'{}'.format(archname), index = False)
            
            a_row = pd.Series(row,index=temp_df.columns)
            mod_df = temp_df.append(a_row,ignore_index = True)
            temp_df = mod_df.sort_values(by='Date')
            i += 1
        else:
            stop = 1

    if stop == 1:
        print('{} activities added for {} {}'.format(i,firsts[user],lasts[user]))
    """
    if gpx_statii[user] == 'Y' and i != 0:
        val = [i]
        
        val_df = pd.DataFrame(columns=['Val'])
        val_row = pd.Series(val,index=val_df.columns)
        mod_val = val_df.append(val_row,ignore_index=True)
        mod_val.to_csv(r'temp-val.csv',index = False)
        
        exec(open('gpxupdate.py').read())
        
        temp_df.to_csv(r'temp-activities.csv',index=False)
        
        try:
            analyse.assess('temp-activities.csv',file_name)
        except:
            print('Error! Work it out!')
        
        os.remove('temp-activities.csv')
        
        os.remove('temp-val.csv')
        
    elif i == 0:
        print('No changes!')
        
    else:
        temp_df.to_csv(r'{}'.format(file_name))
    """
    if i != 0:
        temp_df.to_csv(r'{}'.format(file_name))
    
   
print('Update complete!')
        
    
