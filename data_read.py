#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:18:49 2020

@author: WS
"""

import pandas as pd

from today_string import y_day_string
from datetime import datetime, timedelta

import haversine
import gpxpy
from math import sqrt

import os

cols = ['Activity number','Activity Type','Date','Distance','Time','Shoes','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status']

dist_list = ['1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full']
dist_dict = {'1km': 1000,
              '1 mile': 1609.34,
              '1.5 mile': 2414.02,
              '3 mile': 4828.03,
              '5km': 5000,
              '10km': 10000,
              '20km': 20000,
              'Half': 21097.7,
              'Full': 42195}

def pull_initials():
    user_data = pd.read_csv (r'users.csv')  
 
    users = pd.DataFrame(user_data, columns= ['Initials'])

    initials_list = users['Initials'].tolist()
    
    initials = initials_list[0]
    
    return(initials)

def pull_gpx_status(initials):
    user_data = pd.read_csv (r'users.csv')  
 
    users = pd.DataFrame(user_data, columns= ['GPX'])

    gpx_statii = users['GPX'].tolist()
    
    gpx_status = gpx_statii[0]
    
    return(gpx_status)    

def stringtime_to_floatminute(time_string):
        hours = float(time_string[:2])
        minutes = float(time_string[3:5])
        seconds = float(time_string[6:8])
    
        time = hours * 60 + minutes + seconds/60
    
        return(time)

def pull_data(initials):
    file_name = "{}activities.csv".format(initials)
    
    data = pd.read_csv(r'{}'.format(file_name))
    df = pd.DataFrame(data, columns= cols)
    #df = df.sort_values(by='Date')#sort_values is deprecated Python
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

def activity_splits(user_df,activity_number,distance):
    
    ac_numbers = user_df['Activity number'].tolist()
    splits = user_df[distance].tolist()
    
    split_list = []
    for i in range(0,len(ac_numbers)):
        if ac_numbers[i] == activity_number:
            split_list.append(splits[i])
    
    split = split_list[0]
    
    return(split)
    
def activity_details(user_df,activity_number,field):        
    
    ac_numbers = user_df['Activity number'].tolist()
    types_list = user_df['Activity Type'].tolist()
    dates = user_df['Date'].tolist()
    distances = user_df['Distance'].tolist()
    durs = user_df['Time'].tolist()
    shoes = user_df['Shoes'].tolist()
    
    ac_type = []
    date = []
    dist = []
    dur = []
    shoe = []
    
    for i in range(0,len(ac_numbers)):
        if activity_number == ac_numbers[i]:
            ac_type.append(types_list[i])
            date.append(dates[i])
            dist.append(distances[i])
            dur.append(durs[i])
            shoe.append(shoes[i])
    
    if 'Type' in field:
        value = ac_type[0]
    if 'Date' in field:
        value = date[0]
    if 'Distance' in field:
        value = dist[0]
    if 'Duration' in field or 'Time' in field:
        value = dur[0]
    if 'Shoes' in field:
        value = shoe[0]
    
    return(value)

#user_df = pull_data('WS')
#print(activity_details(user_df,'AB4H2007','Shoes'))
    
def split_rank(user_df,activity_number,distance):
    #df = df.sort_values(by=distance)
    
    #df.to_csv(r'check-sorting.csv')
    
    ac_numbers = user_df['Activity number'].tolist()
    ac_types = user_df['Activity Type'].tolist()
    splits = user_df[distance].tolist()
    
    ac_type = activity_details(user_df,activity_number,'Type')
    split = activity_splits(user_df,activity_number,distance)
    
    n = 1
    stop = 0
    while stop == 0:
        for i in range(0,len(splits)):
            if splits[i] < split and ac_type == ac_types[i]:
                n += 1
            elif activity_number == ac_numbers[i]:
                stop = 1
    
    if split == 'NONE':
        n = 'NONE'
    
    return(n)
            
def split_count(user_df,split):
    
    #ac_numbers = user_df['Activity number'].tolist()
    splits = user_df[split].tolist()
    
    #ac_type = activity_details(user_df,activity_number,'Type')
    
    n = 0
    for i in range(0,len(splits)):
        if splits[i] != 'NONE':
            n += 1           
                
    return(n)

def split_extremes(user_df,distance,extreme):
    
    splits = user_df[distance].tolist()
    
    filter_splits = []
    
    for i in range(0,len(splits)):
        if 'NONE' not in splits[i]:
            filter_splits.append(splits[i])
    
    if 'ax' in extreme:
        output = max(filter_splits)
    
    if 'in' in extreme:
        output = min(filter_splits)
        
    return(output)

def split_percentile(user_df,distance,percentile):
    
    splits = user_df[distance].tolist()
    
    filter_splits = []
    
    for i in range(0,len(splits)):
        if 'NONE' not in splits[i]:
            filter_splits.append(splits[i])
            
    filter_splits.sort()
    
    if percentile > 1:
        percentile = percentile /100
    
    val = round(percentile * len(filter_splits))
    
    if val == len(filter_splits):
        val = val - 1
    
    output = filter_splits[val]
    
    return(output)
    
ws_df = pull_data('WS')
split_percentile(ws_df,'1km',95)
    
    
def latest_activity(initials):
    df = pull_data(initials)
    
    ac_numbers = df['Activity number'].tolist()

    latest = ac_numbers[-1]
    
    return(latest)

""""ROUTE DATA PULL"""

def simple_gpx_pull(filename):
    
    #fileDir = os.path.dirname(os.path.realpath('__file__'))

    #filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.gpx'.format(activity_number))
    
    try:
        gpx_file = open(filename)
        gpx = gpxpy.parse(gpx_file)

        data = gpx.tracks[0].segments[0].points
        
        stop = 0
    except:
        stop = 1
        
    #time_str = str(data[0].time)[:19]
    #time_dt = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')


    df = pd.DataFrame(columns=['lon','lat','alt','time','distance','HR'])
    #df = pd.DataFrame(columns=['lon','lat','alt'])

    dist = [0]

    if stop == 0:
        for i in range(0,len(data)):
            lon = data[i].longitude
            lat = data[i].latitude
            alt = data[i].elevation
            try:
                ext = data.extensions[0].getchildren()[0]
                hr = int(ext.text)
            except:
                hr = 'N/A'
        
            time_str = str(data[i].time)[:19]
            time_dt = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
    
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

    return(df)

def pull_gpx(activity_number):
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))

    filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.gpx'.format(activity_number))
    
    try:
        gpx_file = open(filename)
        gpx = gpxpy.parse(gpx_file)

        data = gpx.tracks[0].segments[0].points
        
        stop = 0
    except:
        stop = 1
        
    #time_str = str(data[0].time)[:19]
    #time_dt = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')


    df = pd.DataFrame(columns=['lon','lat','alt','time','distance','HR'])
    #df = pd.DataFrame(columns=['lon','lat','alt'])

    dist = [0]

    if stop == 0:
        for i in range(0,len(data)):
            lon = data[i].longitude
            lat = data[i].latitude
            alt = data[i].elevation
            try:
                ext = data.extensions[0].getchildren()[0]
                hr = int(ext.text)
            except:
                hr = 'N/A'
        
            time_str = str(data[i].time)[:19]
            time_dt = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
    
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

    return(df)
    
#print(pull_gpx(5221284558))
'''    
def pull_csv(activity_number):
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))

    filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.csv'.format(activity_number))
    
    #I think I only need distance and time
    
    data = pd.read_csv(r'{}'.format(filename))
    old_df = pd.DataFrame(data,columns=['lon','lat','time','distance','HR'])
    
    lats = old_df['lat'].tolist()
    lons = old_df['lon'].tolist()
    dists_un = old_df['distance'].tolist()
    times_un = old_df['time'].tolist()
    hrs = old_df['HR'].tolist()
    
    df = pd.DataFrame(columns=['lon','lat','time','distance','HR'])
    
    for i in range(0,len(times_un)):
        
        time_dt = datetime.strptime(times_un[i],'%Y-%m-%d %H:%M:%S')
        
        row = [lons[i],lats[i],time_dt,dists_un[i],hrs[i]]
        a_row = pd.Series(row,index=df.columns)
        df = df.append(a_row,ignore_index=True)

    return(df)
    
def route_data(activity_number):
    if len(activity_number) == 10:
        df = pull_gpx(activity_number)
    if len(activity_number) == 8 or len(activity_number) == 9:
        df = pull_csv(activity_number)
        
    return(df)
'''

def pull_csv_pd(activity_number,option='column_name'):
    fileDir = os.path.dirname(os.path.realpath('__file__'))

    filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.csv'.format(activity_number))
    
    #I think I only need distance and time
    
    if option == 'column_name':
        data = pd.read_csv(r'{}'.format(filename))
        df = pd.DataFrame(data,columns=['lon','lat','time','distance','HR'])
    else:
        data = pd.read_csv(r'{}'.format(filename))
        df = pd.DataFrame(data,columns=['lon','lat','time','distance','HR',option])
    
    df['time'] = df['time'].apply(lambda x : datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    
    return(df)

def route_data(activity_number,option='column_name'):
    #if len(activity_number) == 10:
    #    df = pull_gpx(activity_number)
    #if len(activity_number) == 8 or len(activity_number) == 9:
    df = pull_csv_pd(activity_number,option)
        
    return(df)    
    