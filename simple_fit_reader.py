#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 17:09:14 2020

@author: WS
"""

import pandas as pd

from fitparse import FitFile

#work out way of importing
fitfile = FitFile('A7OH5840.FIT')

timestamps = []
#note that this is possibly not GMT, or whatever my timezone is now.
heart_rates = []
latitudes = []
longitudes = []
distances = []

# Get all data messages that are of type record
for record in fitfile.get_messages('record'):

    # Go through all the data entries in this record
    for record_data in record:
        
        if record_data.name == 'timestamp':
            timestamps.append(record_data.value)
        if record_data.name == 'position_lat':
            latitudes.append(record_data.value)
        if record_data.name == 'position_long':
            longitudes.append(record_data.value)
        if record_data.name == 'heart_rate':
            heart_rates.append(record_data.value)
        if record_data.name == 'distance':
            distances.append(record_data.value)
        
        """
        # Print the records name and value (and units if it has any)
        if record_data.units:
            print( " * %s: %s %s" % (
                record_data.name, record_data.value, record_data.units,
            ))
        else:
            print (" * %s: %s" % (record_data.name, record_data.value))
        """

df = pd.DataFrame(columns=['time','lat','lon','HR','distance'])

for i in range(0,len(timestamps)):
    
    lat = latitudes[i] * (10 ** (-7))
    lon = longitudes[i] * (10 ** (-7))
    
    row = [timestamps[i],lat,lon,heart_rates[i],distances[i]]
    a_row = pd.Series(row,index=df.columns)
    df = df.append(a_row,ignore_index=True)

time = timestamps[0]
activity_file = 'activity_m{}.csv'.format(time)
    
df.to_csv(r'{}'.format(activity_file))

import analyse

#print(analyse.best_time(1000,df))    

user_data = pd.read_csv (r'users.csv')  
 
users = pd.DataFrame(user_data, columns= ['First name','Last name','Initials','Username','Password','GPX'])

firsts = users['First name'].tolist()
lasts = users['Last name'].tolist()
initials = users['Initials'].tolist()
usernames = users['Username'].tolist()
passwords = users['Password'].tolist()
gpx_statii = users['GPX'].tolist()

file_name = "{}activities.csv".format(initials[0])
    
data = pd.read_csv(r'{}'.format(file_name))
    
if gpx_statii[0] == 'Y':
    archive = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status'])
else:
    archive = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time'])    

from today_string import today_string

archive.to_csv(r'{}{}'.format(today_string,file_name), index = False)

from datetime import timedelta
import time

date = timestamps[0] + timedelta(hours=1)
dist = round((distances[-1]/1000),2)
full_td = timestamps[-1] - timestamps[0]
full_secs = full_td.total_seconds()
full_string = time.strftime('%H:%M:%S',time.gmtime(full_secs))

pace = full_secs/dist

if pace < 181:
    activity = 'Cycling'
if pace >= 181 and pace <= 375:
    activity = 'Running'
if pace > 375:
    activity = 'Walking'

temp_df = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time'])

row = ['MANUAL',activity,date, dist,full_string]
a_row = pd.Series(row,index=temp_df.columns)
temp_df = temp_df.append(a_row,ignore_index=True)

import os

if gpx_statii[0] == 'Y':
    temp_df.to_csv(r'temp-activities.csv',index=False)
        
    analyse.assess('temp-activities.csv',file_name)
        
    os.remove('temp-activities.csv')
                
else:
    temp_df.to_csv(r'{}'.format(file_name))



