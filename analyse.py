#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 14:18:22 2020

@author: WS
"""

import gpxpy
import pandas as pd
from datetime import datetime
import haversine
from math import sqrt

from time import time
from datetime import datetime

import os

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


    df = pd.DataFrame(columns=['lon','lat','alt','time','distance'])
    #df = pd.DataFrame(columns=['lon','lat','alt'])

    dist = [0]

    if stop == 0:
        for i in range(0,len(data)):
            lon = data[i].longitude
            lat = data[i].latitude
            alt = data[i].elevation
        
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

            a_row = [lon,lat,alt,time_dt,distance]
            row = pd.Series(a_row,index=df.columns)
            df = df.append(row,ignore_index = True)

    return(df)

def best_time(distance,gpx_df):
    times = gpx_df['time'].tolist()    
    distances = gpx_df['distance'].tolist()
    full = distances[-1]
    
    distance_times = []
    first = [0]
    
    if len(distances) > 0 and distance < full:
        for i in range(0,len(distances)):
            
            if distances[i] > distance - 1:
                if len(first) == 0:
                    first.append(i)
                
                for v in range(0,i):
                    if (distances[i] - distances[v]) > (distance - 1) and (distances[i] - distances[v]) < (distance + 100):
                        delta = times[i] - times[v]
                        distance_times.append(delta)
            
                if i == int((len(distances)-first[0])/2) and distance > 15000:
                    today = time()
                    today_dt = datetime.fromtimestamp(today)
                    time_string = datetime.strftime(today_dt,'%H:%M:%S')
                    print('50% through {} check at {}'.format(distance,time_string))
            
                if i == int((3 * (len(distances)-first[0]))/4) and distance > 15000:
                    today = time()
                    today_dt = datetime.fromtimestamp(today)
                    time_string = datetime.strftime(today_dt,'%H:%M:%S')
                    print('75% through {} check at {}'.format(distance,time_string))
                
                if i == int((9 * (len(distances)-first[0]))/10) and distance > 15000:
                    today = time()
                    today_dt = datetime.fromtimestamp(today)
                    time_string = datetime.strftime(today_dt,'%H:%M:%S')
                    print('90% through {} check at {}'.format(distance,time_string))
                    
                if i == (len(distances) - 1) and distance > 15000:
                    today = time()
                    today_dt = datetime.fromtimestamp(today)
                    time_string = datetime.strftime(today_dt,'%H:%M:%S')
                    print('{} check completed at {}'.format(distance,time_string))

    if len(distance_times) > 0:
        distance_times.sort()
        best = distance_times[0]
    else:
        best = 'NONE'

    return(best)
        
def best_time_string(time):
    
    if time != 'NONE':
        seconds = time.seconds
    
        mins, secs = divmod(seconds,60)
    
        if secs < 10:
            padding = 0
        else:
            padding = ''
    
        output = '{}m{}{}'.format(mins,padding,secs)
    else:
        output = 'NONE'
    return(output)
    
def best_times_running(gpx_df):
    
    one_k = best_time(1000,gpx_df)
    one_m = best_time(1609.34,gpx_df)
    one_five = best_time(2414.02,gpx_df)
    thr_m = best_time(4828.03,gpx_df)
    fiv_k = best_time(5000,gpx_df)
    ten_k = best_time(10000,gpx_df)
    twe_k = best_time(20000,gpx_df)
    half = best_time(21097.7,gpx_df)
    full = best_time(42195,gpx_df)
    
    times = [one_k, one_m, one_five, thr_m, fiv_k, ten_k, twe_k, half, full]
    print(times)
    return(times)
    
def best_times_cycling(gpx_df):
    #check_list = gpx_df['distance'].tolist()
    
    #if check_list[-1] < 50000:
    #   ten_k = best_time(10000,gpx_df)
    #else:
    #    ten_k = 'LONG'
    ten_k = best_time(10000,gpx_df)
    twe_k = best_time(20000,gpx_df)
    fif_k = best_time(50000,gpx_df)
    hun_k = best_time(100000,gpx_df)
    t_h_k = best_time(200000,gpx_df)
    t_f_k = best_time(250000,gpx_df)
    
    times = [ten_k, twe_k, fif_k, hun_k, t_h_k, t_f_k]
    print(times)
    return(times)

def printable(times):
    output = []
    for i in range(0,len(times)):
        string = best_time_string(times[i])
        output.append(string)
    return(output)
    
    

    
    
    
    
    
    
    