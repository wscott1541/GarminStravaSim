#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:18:49 2020

@author: WS
"""

import pandas as pd

from today_string import y_day_string
from datetime import datetime, timedelta

import os

user_data = pd.read_csv (r'users.csv')  
 
users = pd.DataFrame(user_data, columns= ['Initials'])

initials_list = users['Initials'].tolist()

def stringtime_to_floatminute(time_string):
        hours = float(time_string[:2])
        minutes = float(time_string[3:5])
        seconds = float(time_string[6:8])
    
        time = hours * 60 + minutes + seconds/60
    
        return(time)

cols = ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status']

def pull_data(initials):
    file_name = "{}activities.csv".format(initials)
    
    data = pd.read_csv(r'{}'.format(file_name))
    df = pd.DataFrame(data, columns= cols)
    df = df.sort_values(by='Date')#sort_values is deprecated Python
    return(df)

def data_read(initials):
    df = pull_data(initials)

    dates_times = df['Date'].tolist()
    dates = []
    for i in range(0,len(dates_times)):
        useful_dates = dates_times[i][0:10]
        dates.append(useful_dates)#in format string 'yyyy-mm-dd'
    #I don't know if this is even necessary, but I don't want to try to amend every this to working in datetime

    """    
    from datetime import datetime
    new_dates = []
    for i in range(0,len(dates)):
        datetime_strp = datetime.strptime(dates_times[i],'%Y-%m-%d %H:%M:%S')
        datetime_object = datetime.timestamp(datetime_strp)
        new_dates.append(datetime_object)

    """

    #make distances useable
    distances = df['Distance'].tolist()

    #make durations useable
    #duration_times = df['Time'].tolist()
    duration_strings = df['Time'].tolist()
    
    durations = []
    for i in range(0,len(duration_strings)):
        dur = stringtime_to_floatminute(duration_strings[i])
        durations.append(dur)
    
    types = df['Activity Type'].tolist()
    
    return(dates,distances,durations,types)
    
def all_times(initials,distance):
    df = pull_data(initials)
    
    types = df['Activity Type'].tolist()
    dates = df['Date'].tolist()
    dists = df['Distance'].tolist()
    splits = df[distance].tolist()
    
    return(types,dates,dists,splits)
    
def week_times(initials,distance):
    all_types,all_dates,all_dists,all_splits = all_times(initials,distance)
    
    y_day_obj = datetime.strptime(y_day_string,'%Y-%m-%d')
    
    last_week = y_day_obj - timedelta(days=7)
    
    types = []
    dates = []
    dists = []
    splits = []
    
    for i in range(0,len(all_dates)):
        stamp = all_dates[i][:10]
        obj = datetime.strptime(stamp,'%Y-%m-%d')
        
        if obj > last_week:
            types.append(all_types[i])
            dates.append(all_dates[i])
            dists.append(all_dists[i])
            splits.append(all_splits[i])
            
    return(types,dates,dists,splits)

     
        
    
    