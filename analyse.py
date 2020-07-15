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
                if len(first) == 1:
                    first.append(i)
                
                for v in range(0,i):
                    if (distances[i] - distances[v]) > (distance - 1) and (distances[i] - distances[v]) < (distance + 100):
                        delta = times[i] - times[v]
                        distance_times.append(delta)
            
                if i == int((len(distances)-first[1])/2) and distance > 15000:
                    today = time()
                    today_dt = datetime.fromtimestamp(today)
                    time_string = datetime.strftime(today_dt,'%H:%M:%S')
                    print('50% through {} check at {}'.format(distance,time_string))
            
                if i == int((3 * (len(distances)-first[1]))/4) and distance > 15000:
                    today = time()
                    today_dt = datetime.fromtimestamp(today)
                    time_string = datetime.strftime(today_dt,'%H:%M:%S')
                    print('75% through {} check at {}'.format(distance,time_string))
                
                if i == int((9 * (len(distances)-first[1]))/10) and distance > 15000:
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
    
def remove_padding(time):
    if time[0] == '0':
        time = time[1]
    return(time)
        
def best_time_string(time):
    try:
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
    except:
        if time != 'NONE':
            time = time[7:]
            time_object = datetime.strptime(time,'%H:%M:%S')
            hours = remove_padding(datetime.strftime(time_object,'%H'))
            mins = datetime.strftime(time_object,'%M')
            secs = (datetime.strftime(time_object,'%S'))

            if hours == '0':
                mins = remove_padding(mins)
                output = '{}m{}'.format(mins,secs) 
            else:
                output = '{}h{}m{}'.format(hours,mins,secs)       
        else:
            output= 'NONE'

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

def assess(temporary,main):
    if temporary[-4:] != '.csv':
        temporary = temporary + '.csv'
    if main[-4:] != '.csv':
        main = main + '.csv'    
    
    data = pd.read_csv(r'{}'.format(temporary))

    df = pd.DataFrame(data,columns= ['Activity number','Activity Type','Date','Distance','Time'])

    try:
        new_data = pd.read_csv(r'{}'.format(main))
        new = pd.DataFrame(new_data,columns= ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status'])
        prev = 1
        statii = new['Status'].tolist()
        starts = []
        for n in range(0,len(statii)):
            if statii[n] != 'Y' and statii[n] != 'NONE':
                starts.append(n)
        
        #prev_activities = new['Activity number'].tolist()
    except:
        new = pd.DataFrame(columns= ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status'])
        prev = 0

    activities = df['Activity number'].tolist()
    types = df['Activity Type'].tolist()
    dates = df['Date'].tolist()
    dists = df['Distance'].tolist()
    times = df['Time'].tolist()

    if prev == 1:
        start = starts[0]
        ran = range(start-2,len(activities))
    else:
        ran = range(0,len(activities))

    for i in ran:
        if prev == 1:
            try:
                if statii[i] == 'Y' or statii[i] == 'NONE':
                    skip = 1
                else:
                    skip = 0
            except:
                skip = 0
        else:
            skip = 0
            
    
        if skip == 0:
            print('Loading activity',i)
            ac_no = activities[i]
    
            row = [ac_no,types[i],dates[i],dists[i],times[i]]
    
            #gpx_df = analyse.pull_gpx(ac_no)
            
            #r_times = analyse.best_times_running(gpx_df)
                    #[one_k, one_m, one_five, thr_m, fiv_k, ten_k, twe_k, half, full]
                    #c_times = analyse.best_times_cycling(gpx_df)
                    #[ten_k, twe_k, fif_k, hun_k, t_h_k, t_f_k]
            
            if row[1] != 'Running' and row[1] != 'Cycling':
                r_times = ['NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE']
                c_times = ['NONE','NONE','NONE','NONE','NONE','NONE']
                status = 'NONE'
            else:
                fileDir = os.path.dirname(os.path.realpath('__file__'))

                filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.gpx'.format(ac_no))
        
                size = os.stat(filename).st_size
                print(size)
        
                if size > 0:
                    today = time()
                    today_dt = datetime.fromtimestamp(today)
                    time_string = datetime.strftime(today_dt,'%H:%M:%S')
                    print('Reading activity {} GPX at {}'.format(i,time_string))
                    gpx_df = pull_gpx(row[0])
                    today = time()
                    today_dt = datetime.fromtimestamp(today)
                    time_string = datetime.strftime(today_dt,'%H:%M:%S')
                    print('Read activity {} GPX at {}'.format(i,time_string))
                    status = 'Y'
                else:
                    status = 'INVALID'
            
            if row[1] == 'Running':
                r_times = best_times_running(gpx_df)
            else:
                r_times = ['NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE']
                #[one_k, one_m, one_five, thr_m, fiv_k, ten_k, twe_k, half, full]
            if row[1] == 'Cycling':
                c_times = best_times_cycling(gpx_df)
            else:
                c_times = ['NONE','NONE','NONE','NONE','NONE','NONE']
                        #[ten_k, twe_k, fif_k, hun_k, t_h_k, t_f_k]
            new_row = [row[0],row[1],row[2],row[3],row[4],r_times[0],r_times[1],r_times[2],r_times[3],r_times[4],r_times[5],r_times[6],r_times[7],r_times[8],c_times[0],c_times[1],c_times[2],c_times[3],c_times[4],c_times[5],status]
            
            #a_row = pd.Series(new_row,index=new.columns)#this should be done with a replace if the activity exists, else append
            #mod_df = new.append(a_row,ignore_index = True)
            #new = mod_df.sort_values(by='Date')
            new.iloc[i] = new_row
            new.to_csv(r'{}'.format(main),index=False)  
  
def personal_best(category,activities_csv):
    data = pd.read_csv(r'{}'.format(activities_csv))
    df = pd.DataFrame(data,columns= [category])
    
    times_unfiltered = df[category].tolist()
    
    times = []
    
    for i in range(0,len(times_unfiltered)):
        if times_unfiltered[i] != 'NONE':
            times.append(times_unfiltered[i])
    
    if len(times) > 0:
        times.sort()
        best = best_time_string(times[0])
    else:
        best = 'NONE'
    
    return(best)
    
def listing_append(df,string_list,stop):
    full = []
    for i in range(0,len(string_list)):
        col = df[string_list[i]].tolist
        full.append(col)
    
    output_df = pd.DataFrame(columns=string_list)
    
    print(stop)
    
    for i in range(0,stop):
        print(i)
        row = []
        for n in range(0,len(full)):
            unpack_item_list = full[n]
            unpack_item = unpack_item_list[i]
            row.append(unpack_item)
        
        a_row = pd.Series(row,index=output_df.columns)#this should be done with a replace if the activity exists, else append
        output_df = output_df.append(a_row,ignore_index = True)
    
    return(output_df)  
    
def assess_test(temporary,main):
    if temporary[-4:] != '.csv':
        temporary = temporary + '.csv'
    if main[-4:] != '.csv':
        main = main + '.csv'    
    
    data = pd.read_csv(r'{}'.format(temporary))

    df = pd.DataFrame(data,columns= ['Activity number','Activity Type','Date','Distance','Time'])

    #try:
    mid_data = pd.read_csv(r'{}'.format(main))
    mid = pd.DataFrame(mid_data,columns= ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status'])
    prev = 1
    statii = mid['Status'].tolist()
    starts = []
    for n in range(0,len(statii)):
        if statii[n] != 'Y' and statii[n] != 'NONE':
            starts.append(n)
    start = starts[0]-1
    
        #new = pd.DataFrame(columns= ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status'])        
        
    listing = ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status']
        
    new = listing_append(mid,listing,start)
        
        #prev_activities = new['Activity number'].tolist()
    """
    except:
        new = pd.DataFrame(columns= ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status'])
        prev = 0
"""
    activities = df['Activity number'].tolist()
    types = df['Activity Type'].tolist()
    dates = df['Date'].tolist()
    dists = df['Distance'].tolist()
    times = df['Time'].tolist()

    if prev == 1:
        ran = range(start-2,len(activities))
    else:
        ran = range(0,len(activities))

    for i in ran:
        if prev == 1:
            try:
                if statii[i] == 'Y' or statii[i] == 'NONE':
                    skip = 1
                else:
                    skip = 0
            except:
                skip = 0
        else:
            skip = 0
            
    
        if skip == 0:
            print('Loading activity',i)
            ac_no = activities[i]
    
            row = [ac_no,types[i],dates[i],dists[i],times[i]]
    
            #gpx_df = analyse.pull_gpx(ac_no)
            
            #r_times = analyse.best_times_running(gpx_df)
                    #[one_k, one_m, one_five, thr_m, fiv_k, ten_k, twe_k, half, full]
                    #c_times = analyse.best_times_cycling(gpx_df)
                    #[ten_k, twe_k, fif_k, hun_k, t_h_k, t_f_k]
            
            if row[1] != 'Running' and row[1] != 'Cycling':
                r_times = ['NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE']
                c_times = ['NONE','NONE','NONE','NONE','NONE','NONE']
                status = 'NONE'
            else:
                fileDir = os.path.dirname(os.path.realpath('__file__'))

                filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.gpx'.format(ac_no))
        
                size = os.stat(filename).st_size
                print(size)
        
                if size > 0:
                    today = time()
                    today_dt = datetime.fromtimestamp(today)
                    time_string = datetime.strftime(today_dt,'%H:%M:%S')
                    print('Reading activity {} GPX at {}'.format(i,time_string))
                    gpx_df = pull_gpx(row[0])
                    today = time()
                    today_dt = datetime.fromtimestamp(today)
                    time_string = datetime.strftime(today_dt,'%H:%M:%S')
                    print('Read activity {} GPX at {}'.format(i,time_string))
                    status = 'Y'
                else:
                    status = 'INVALID'
            
            if row[1] == 'Running':
                r_times = best_times_running(gpx_df)
            else:
                r_times = ['NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE']
                #[one_k, one_m, one_five, thr_m, fiv_k, ten_k, twe_k, half, full]
            if row[1] == 'Cycling':
                c_times = best_times_cycling(gpx_df)
            else:
                c_times = ['NONE','NONE','NONE','NONE','NONE','NONE']
                        #[ten_k, twe_k, fif_k, hun_k, t_h_k, t_f_k]
            new_row = [row[0],row[1],row[2],row[3],row[4],r_times[0],r_times[1],r_times[2],r_times[3],r_times[4],r_times[5],r_times[6],r_times[7],r_times[8],c_times[0],c_times[1],c_times[2],c_times[3],c_times[4],c_times[5],status]
    
            a_row = pd.Series(new_row,index=new.columns)#this should be done with a replace if the activity exists, else append
            mod_df = new.append(a_row,ignore_index = True)
            new = mod_df.sort_values(by='Date')
            new.to_csv(r'{}'.format(main),index=False)  
    
    
    
    
    