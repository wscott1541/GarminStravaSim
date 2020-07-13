#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:18:49 2020

@author: WS
"""

import pandas as pd

user_data = pd.read_csv (r'users.csv')  
 
users = pd.DataFrame(user_data, columns= ['Initials'])

initials_list = users['Initials'].tolist()

def stringtime_to_floatminute(time_string):
        hours = float(time_string[:2])
        minutes = float(time_string[3:5])
        seconds = float(time_string[6:8])
    
        time = hours * 60 + minutes + seconds/60
    
        return(time)

def data_read(initials):
    file_name = "{}activities.csv".format(initials)
    
    data = pd.read_csv(r'{}'.format(file_name))
    df = pd.DataFrame(data, columns= ['Activity Type','Date','Distance','Time'])
    df = df.sort_values(by='Date')#sort_values is deprecated Python

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