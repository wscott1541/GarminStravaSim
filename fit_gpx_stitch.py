#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 09:07:15 2020

@author: WS
"""

import pandas as pd

import os

from today_string import today_string

from datetime import timedelta
import time

from fitparse import FitFile

import gpxpy

from datetime import datetime
import haversine
from math import sqrt

#time_str = str(data[0].time)[:19]
#time_dt = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')

ac_abbr = 'M20201121'# in format M'Date'

fit_file = 'ABKI0905.FIT'

fitfile = FitFile(fit_file)

fit_ts = []
fit_hr = []

for record in fitfile.get_messages('record'):

    # Go through all the data entries in this record
    for record_data in record:
        
        #print(record_data)
        
        if record_data.name == 'timestamp':
            fit_ts.append(record_data.value)
        if record_data.name == 'heart_rate':
            fit_hr.append(record_data.value)
            


gpx_file = 'Evening_Run_(1).gpx'

try:
    gpx_file = open(gpx_file)
    gpx = gpxpy.parse(gpx_file)

    data = gpx.tracks[0].segments[0].points
        
    stop = 0
except:
    stop = 1

df = pd.DataFrame(columns=['lon','lat','alt','time','distance','HR'])
#df = pd.DataFrame(columns=['lon','lat','alt'])

dist = [0]

timestamps = []

if stop == 0:
    for i in range(0,len(data)):
        lon = data[i].longitude
        lat = data[i].latitude
        alt = data[i].elevation
        #try:
        #    ext = data.extensions[0].getchildren()[0]
        #    hr = int(ext.text)
        #except:
        #    hr = 'N/A'
        
        time_str = str(data[i].time)[:19]
        time_dt = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
        timestamps.append(time_dt)
        
        hr_found = False
        
        hrs = []
        
        while hr_found == False:
            
            for n in range(0,len(fit_ts)):
                if time_dt == fit_ts[n]:
                    hrs.append(fit_hr[n])
                    hr_found = True   
                    #print('HR found: ',time_dt)

        hr = hrs[0]

        if i > 0:
            prev_lon = data[i-1].longitude
            prev_lat = data[i-1].latitude
            prev_alt = data[i-1].elevation
                
            delta_2D = haversine.haversine((prev_lat,prev_lon),(lat,lon)) * 1000
                    
            delta_alt = alt - prev_alt
                    
            distance_3D = sqrt((delta_2D ** 2) + (delta_alt ** 2))
                
            new = dist[-1] + distance_3D
        
            dist.append(new)
                
        distance = dist[-1]

        a_row = [lon,lat,alt,time_dt,distance,hr]
        row = pd.Series(a_row,index=df.columns)
        df = df.append(row,ignore_index = True)

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
full_dist = round((dist[-1]/1000),2)
full_td = timestamps[-1] - timestamps[0]
full_secs = full_td.total_seconds()
full_string = time.strftime('%H:%M:%S',time.gmtime(full_secs))

pace = full_secs/full_dist

if pace < 181:
    activity = 'Cycling'
if pace >= 181 and pace <= 570:
    activity = 'Running'
if pace > 570:
    activity = 'Walking'

shoes = 'Hoka One One Clifton 6'    
#activity = 'Kayaking'
#activity = 'Cardio'
    
abbr_df = pd.DataFrame(columns=['abbr','type'])
abbr_row = pd.Series([ac_abbr],index=abbr_df.columns)
mod_abbr = abbr_df.append(abbr_row,ignore_index=True)
mod_abbr.to_csv(r'temp-abbr.csv',index = False)
    
#ac_check = input('Was this a {} activity? (Y/N) '.format(activity))

#if ac_check == 'N':
#    print('Pace: ',pace)
#    activity = input('Activity: ')

temp_df = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time','Shoes'])

row = [ac_abbr,activity,date, full_dist,full_string,shoes]
a_row = pd.Series(row,index=temp_df.columns)
temp_df = temp_df.append(a_row,ignore_index=True)

if gpx_statii[0] == 'Y':
    temp_df.to_csv(r'temp-activities.csv',index=False)
        
    analyse.assess('temp-activities.csv',file_name)
        
    os.remove('temp-activities.csv')
    
else:
    temp_df.to_csv(r'{}'.format(file_name))

print('Processing email...')

import map_email_gen

try:
    os.remove(f'{fit_file}.FIT')
except:
    print('No FIT file')
    
try:
    os.remove(f'{gpx_file}.FIT')
except:
    print('No gpx file')

try:
    os.remove('temp-abbr.csv')
except:
    print('Complete!') 