#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 17:09:14 2020

@author: WS
"""

import os

import pandas as pd

from fitparse import FitFile

from today_string import today_string

from datetime import timedelta
import time

#ac_file = input('activity_file_name.FIT: ')

ac_file = 'AB5G2247.FIT'

if len(ac_file) == 44:
    ac_file = ac_file[-12:]

ac_abbr = ac_file[:-4]

fitfile = FitFile(ac_file)

timestamps = []
#note that this is possibly not GMT, or whatever my timezone is now.
heart_rates = []
latitudes = []
longitudes = []
distances = []
cadences = []

# Get all data messages that are of type record
for record in fitfile.get_messages('record'):

    # Go through all the data entries in this record
    for record_data in record:
        
        #print(record_data)
        
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
        if record_data.name == 'cadence':
            cadences.append(record_data.value)
            
        
        """
        # Print the records name and value (and units if it has any)
        if record_data.units:
            print( " * %s: %s %s" % (
                record_data.name, record_data.value, record_data.units,
            ))
        else:
            print (" * %s: %s" % (record_data.name, record_data.value))
        
        
        #cadence, distance,enhanced_speed,heart_rate,lat,lon,speed,timestamp, unknown_88
        """


df = pd.DataFrame(columns=['time','lat','lon','HR','distance','cadence'])

lat_breaks = []
lat_break_checks = []
lon_breaks = []
lon_break_checks = []

for i in range(0,len(timestamps)):
    
    #blank out and add lat/lon if cardio
    
    try:
        lat = latitudes[i] / (10 ** (7))
    except:
        if len(lat_breaks) == 0:
            lat_breaks.append(latitudes[i-1] / (10 ** (7)))
        elif lat_break_checks[-1] == i - 1:
            here = 'junk'
        else:
            lat_breaks = [latitudes[i-1] / (10 ** (7))]
        lat_break_checks.append(i)
        
        lat = lat_breaks[0]
    try:
        lon = longitudes[i] * (10 ** (-7))
    except:
        if len(lon_breaks) == 0:
            lon_breaks.append(longitudes[i-1] / (10 ** (7)))
        elif lon_break_checks[-1] == i - 1:
            here = 'junk'
        else:
            lon_breaks = [longitudes[i-1] / (10 ** (7))]
        lon_break_checks.append(i)    
        
        lon = lon_breaks[0]
    
    
    #lat = 'NONE'
    #lon = 'NONE'
    
    timestamp = timestamps[i] + timedelta(hours=1)
        
    row = [timestamp,lat,lon,heart_rates[i],distances[i],cadences[i]]
    a_row = pd.Series(row,index=df.columns)
    df = df.append(a_row,ignore_index=True)

#time = timestamps[0]

fileDir = os.path.dirname(os.path.realpath('__file__'))

filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.csv'.format(ac_abbr))
    
df.to_csv(r'{}'.format(filename))

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
    archive = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time','Shoes','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status'])
else:
    archive = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time'])    

#initial archiving
archive = pd.DataFrame(data)
archname = os.path.join(fileDir, 'Archive.gitignore/{}{}'.format(today_string,file_name))
archive.to_csv(r'{}'.format(archname), index = False)

date = timestamps[0] + timedelta(hours=1)
dist = round((distances[-1]/1000),2)
full_td = timestamps[-1] - timestamps[0]
full_secs = full_td.total_seconds()
full_string = time.strftime('%H:%M:%S',time.gmtime(full_secs))

pace = full_secs/dist

if pace < 181:
    activity = 'Cycling'
    shoes = 'NONE'
if pace >= 181 and pace <= 570:
    activity = 'Running'
    shoes = 'Hoka One One Clifton 6'
if pace > 570:
    activity = 'Walking'
    shoes = 'Merrell Vego 2019'
    
#activity = 'Kayaking'
#activity = 'Cardio'
#shoes = 'NONE'
    
abbr_df = pd.DataFrame(columns=['abbr','type'])
abbr_row = pd.Series([ac_abbr],index=abbr_df.columns)
mod_abbr = abbr_df.append(abbr_row,ignore_index=True)
mod_abbr.to_csv(r'temp-abbr.csv',index = False)
    
#ac_check = input('Was this a {} activity? (Y/N) '.format(activity))

#if ac_check == 'N':
#    print('Pace: ',pace)
#    activity = input('Activity: ')

temp_df = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time','Shoes'])

row = [ac_abbr,activity,date, dist,full_string,shoes]
a_row = pd.Series(row,index=temp_df.columns)
temp_df = temp_df.append(a_row,ignore_index=True)

if gpx_statii[0] == 'Y':
    temp_df.to_csv(r'temp-activities.csv',index=False)
    
    #print('pre_assess')    
    analyse.assess('temp-activities.csv',file_name)
        
    os.remove('temp-activities.csv')
    
else:
    temp_df.to_csv(r'{}'.format(file_name))

print('Processing email...')

import map_email_gen

try:
    os.remove(f'{ac_abbr}.FIT')
except:
    print('No FIT file')

try:
    os.remove('temp-abbr.csv')
except:
    print('Complete!')    