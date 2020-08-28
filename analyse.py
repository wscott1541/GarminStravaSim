#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 14:18:22 2020

@author: WS
"""

#column reference: ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status']

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
    if len(activity_number) == 8:
        df = pull_csv(activity_number)
        
    return(df)
    
#print(route_data('A81A2327'))

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
            if statii[n] != 'GPX' and statii[n] != 'NONE' and statii[n] != 'CSV':
                starts.append(n)
        if len(starts) == 0:
            starts.append(len(statii))
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
                if statii[i] == 'GPX' or statii[i] == 'NONE' or statii[i] == 'CSV':
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
                
                if len(ac_no) == 10:
                
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
                        status = 'GPX'
                    else:
                        status = 'INVALID'
                    
                elif len(ac_no) == 8:
                    filename = 'activity_{}.csv'.format(ac_no)
                    gpx_df = pull_csv(ac_no)
                    status = 'CSV'
            
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
            try:
                new.iloc[i] = new_row
            except:
                a_row = pd.Series(new_row,index=new.columns)#this should be done with a replace if the activity exists, else append
                mod_df = new.append(a_row,ignore_index = True)
                new = mod_df.sort_values(by='Date')
            new.to_csv(r'{}'.format(main),index=False)  
    
import matplotlib.pyplot as plt

def hr_plot_time(df):

    try:
        times_un = df['time'].tolist()
        hrs = df['HR'].tolist()
    except:
        new = route_data(df)
        times_un = new['time'].tolist()
        hrs = new['HR'].tolist()
    
    times = []
    for i in range(0,len(times_un)):
        if i == 0:
            times.append(0)
        else:
            full_td = times_un[i] - times_un[0]
            full_secs = full_td.total_seconds()
            times.append(full_secs)
        
    max_hr = 220 - 26
    
    avg_hr = sum(hrs)/len(hrs)
    plt.plot([0,times[-1]],[avg_hr,avg_hr],':',color='black')
    
    for i in range(1,len(times)):
        if hrs[i-1] < (0.6 * max_hr):
            fill_color = 'blue'
        if hrs[i-1] >= (0.6 * max_hr) and hrs[i] < (0.7 * max_hr):
            fill_color = 'green'
        if hrs[i-1] >= (0.7 * max_hr) and hrs[i] < (0.8 * max_hr):
            fill_color = 'yellow'
        if hrs[i-1] >= (0.8 * max_hr) and hrs[i] < (0.9 * max_hr):
            fill_color = 'orange'
        if hrs[i-1] >= (0.9 * max_hr):
            fill_color = 'red'
        
        xs = [times[i-1],times[i]]
        ys = [hrs[i-1],hrs[i]]
        
        try:
            plt.plot(xs,ys,color=fill_color)
        except:
            print('Breaks at {}'.format(i))
    
    plt.xlabel('Duration (s)')
    plt.ylabel('HR (bpm)')
    
    #plt.plot(times,hrs)

#plt.show()
#route = route_data('A8PF0657')
#hr_plot_time(route)


def hr_plot_dist(df):
    try:
        dists = df['distance'].tolist()
        hrs = df['HR'].tolist()
    except:
        new = route_data(df)
        dists = new['distance'].tolist()
        hrs = new['HR'].tolist()
    
    for i in range(1,len(dists)):
        if hrs[i-1] < 120:
            fill_color = 'green'
        if hrs[i-1] >= 120 and hrs[i] < 155:
            fill_color = 'blue'
        if hrs[i-1] >= 155:
            fill_color = 'red'
        
        xs = [dists[i-1],dists[i]]
        ys = [hrs[i-1],hrs[i]]
        
        plt.plot(xs,ys,color=fill_color)
    
    plt.xlabel('Distance (m)')
    plt.ylabel('HR (bpm)')
    
    #plt.plot(dists,hrs)

#plt.show()    
#route = route_data('A85I1222')
#hr_plot_time(route)
#plt.show()
#hr_plot_dist(route)
#plt.show()

def hr_dist_speed_plot(df):
    dists = df['distance'].tolist()
    hrs = df['HR'].tolist()
    times_un = df['time'].tolist()
    
    speeds = []
    for i in range(0,len(times_un)):
        if i < 30:
            speeds.append(0)
        else:
            full_td = times_un[i] - times_un[i-30]
            full_secs = full_td.total_seconds()
            speed = ((dists[i]-dists[i-30])/full_secs) * 3.6
            speeds.append(speed)
            
    fig,ax = plt.subplots()
    ax.plot(dists,hrs,color='blue',label='HR (bpm)')
    
    ax.set_xlabel('Distance (m)')
    ax.set_ylabel('HR (bpm)')
    
    ax2=ax.twinx()
    
    ax2.plot(dists,speeds,':',color='orange',label='Speed (km/h)')
    ax2.set_ylabel('Speed (km/h)')
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width, box.height])
    ax.legend(loc='upper center', bbox_to_anchor=(0.3, 1.14))
    
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0, box.width, box.height])
    ax2.legend(loc='upper center', bbox_to_anchor=(0.75, 1.14))
    
    #ax2.plot(dists,paces)
    
def hr_dist_durs_plot(df):
    dists = df['distance'].tolist()
    hrs = df['HR'].tolist()
    times_un = df['time'].tolist()
    
    times = []
    for i in range(0,len(times_un)):
        if i == 0:
            times.append(0)
        else:
            full_td = times_un[i] - times_un[0]
            full_secs = full_td.total_seconds()
            times.append(full_secs)
    
    max_hr = 220 - 26
    zone_thr = 0.7 * max_hr
    zone_fou = 0.8 * max_hr
    zone_fiv = 0.9 * max_hr
    
    min_hr = min(hrs)
    max_hr = max(hrs)
    xs = [0,dists[-1]]
    
    fig,ax = plt.subplots()
    
    if min_hr < zone_thr:
        ax.plot(xs,[zone_thr,zone_thr],':',color='orange')
    if max_hr > zone_fou:
        ax.plot(xs,[zone_fou,zone_fou],':',color='orange')
    if max_hr > zone_fiv:
        ax.plot(xs,[zone_fiv,zone_fiv],':',color='orange')    
        
    ax.plot(dists,hrs,color='blue',label = 'Distance (m)')
    
    #ax.set_xlabel('Distance (m)')
    ax.set_ylabel('HR (bpm)')
    
    plt.xlim([0,dists[-1]])
    
    ax2=ax.twiny()
    
    ax2.plot(times,hrs,color='red',label='Durations (s)')
    #ax2.set_xlabel('Duration (s)')
    
    ax.legend();
    ax2.legend();
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width, box.height])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.06))
    
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0, box.width, box.height])
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2))
    
    plt.xlim([0,times[-1]])
    
    plt.ylim([min_hr-5,max_hr+5])
    
    #ax2.plot(dists,paces)
    
def hr_zones_pie(df):
    hrs = df['HR'].tolist()
    #times_un = df['time'].tolist()
    
    zone_one = []
    zone_two = []
    zone_thr = []
    zone_fou = []
    zone_fiv = []
    
    max_hr = 220 - 26
    
    for i in range(0,len(hrs)):
        if hrs[i] < max_hr * 0.6:
            zone_one.append(hrs[i])
        if hrs[i] >= max_hr * 0.6 and hrs[i] < max_hr * 0.7:
            zone_two.append(hrs[i])
        if hrs[i] >= max_hr * 0.7 and hrs[i] < max_hr * 0.8:
            zone_thr.append(hrs[i])
        if hrs[i] >= max_hr * 0.8 and hrs[i] < max_hr * 0.9:
            zone_fou.append(hrs[i])
        if hrs[i] >= max_hr * 0.9:
            zone_fiv.append(hrs[i])
    
    zone_labels = []
    zone_values = []
    
    if len(zone_one) > len(hrs) * 0.02:
        amount_s = len(zone_one)
        mins,secs = divmod(amount_s,60)
        zone_labels.append(f'Zone 1: {mins}m{secs}s')
        zone_values.append(len(zone_one))
    if len(zone_two) > len(hrs) * 0.02:
        amount_s = len(zone_two)
        mins,secs = divmod(amount_s,60)
        zone_labels.append(f'Zone 2: {mins}m{secs}s')
        zone_values.append(len(zone_two))
    if len(zone_thr) > len(hrs) * 0.02:
        amount_s = len(zone_thr)
        mins,secs = divmod(amount_s,60)
        zone_labels.append(f'Zone 3: {mins}m{secs}s')
        zone_values.append(len(zone_thr))
    if len(zone_fou) > len(hrs) * 0.02:
        amount_s = len(zone_fou)
        mins,secs = divmod(amount_s,60)
        zone_labels.append(f'Zone 4: {mins}m{secs}s')
        zone_values.append(len(zone_fou))
    if len(zone_fiv) > len(hrs) * 0.02:
        amount_s = len(zone_fiv)
        mins,secs = divmod(amount_s,60)
        zone_labels.append(f'Zone 5: {mins}m{secs}s')
        zone_values.append(len(zone_fiv))
        
     
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.axis('equal')
    #zone_labels = ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5']
    #zones = [len(zone_one),len(zone_two),len(zone_thr),len(zone_fou),len(zone_fiv)]
    plt.pie(zone_values, labels = zone_labels,autopct='%1.2f%%')

#plt.show()
#route = route_data('A8PF0657')
#hr_dist_speed_plot(route)
#plt.show()

def lap_bars(df):
    
    dists = df['distance'].tolist()
    times_un = df['time'].tolist()
    #times = []
    
    n = 1
    markers = [0]
    
    for i in range(0,len(dists)):
        #time = times_un[i].total_seconds()
        #times.append(time)
        
        if dists[i-1] < (n * 1000) and dists[i] > (n * 1000):
            markers.append(i-1)
            
            n += 1
    
    markers.append(len(times_un)-1)
    
    order = []
    r_lap_times = []
    r_labels = []
    
    for i in range(1,len(markers)):
        sta = markers[i-1]
        fin = markers[i]
        lap_time_s = (times_un[fin]-times_un[sta]).total_seconds()
        lap_time_m = lap_time_s/60
        r_lap_times.append(lap_time_m)
        order.append(i)
        if i < len(markers):
            label = f'{i-1}-{i}km'
        else:
            fin = round((dists[-1]/1000),2)
            label = f'{i-1}-{fin}km'
        r_labels.append(label)
    
    lap_times = []
    labels = []
    
    for i in range(0,len(order)):
        tot = len(order)-1
        #order.append(t_order[tot-i])
        lap_times.append(r_lap_times[tot-i])
        labels.append(r_labels[tot-i])
        
    plt.barh(order,lap_times)
    
    plt.xlabel("Time (mins)")
    plt.yticks(order,labels)
    

def words(activity_type):
    
    if activity_type == 'Running':
        noun = 'run'
        verb = 'ran'
        plural = 'runs'
    elif activity_type == 'Cycling':
        noun = 'cycle'
        verb = 'cycled'
        plural = 'cycles'
    elif activity_type == 'Walking' or activity_type == 'Hiking':
        noun = 'walk'
        verb = 'walked'
        plural = 'walks'
    elif activity_type == 'Cardio':
        noun = 'Cardio'
        verb = 'worked out'
        plural = 'work outs'
    else:
        pos = activity_type.find('ing')
        base = activity_type[:pos]
        noun = base
        verb = base + 'ed'
        plural = base + 's'
    
    return(noun,verb,plural)

def hr_distribution(df):
    hrs = df['HR'].tolist()
    
    hr_max = max(hrs)

    hr_min = min(hrs)

    xs = []
    ys = []
    
    for i in range(hr_min,hr_max+1):
        n = 0
        hr = i
        for v in range(0,len(hrs)):
            if hrs[v] == hr:
                n += 1
                
        xs.append(hr)
        ys.append(n)
    
    max_hr = 220 - 26
    
    mean = sum(hrs)/len(hrs)
    #mode_vals = [0]
    
    #for i in range(0,len(ys)):
    #    if ys[i] > mode_vals[-1]:
    #        mode_vals.append(i)
    #        
    #mode = xs[(mode_vals[-1])] - 1 
    
    mode_vals = []
    
    for i in range(0,len(ys)):
        if ys[i] == max(ys):
            mode_vals.append(i)
            
    mode = xs[mode_vals[0]]
    
    median_val = int(sum(ys)/2)
    median_sum = [ys[0]]
    median_vals = []
    
    for i in range(1,len(ys)):
        if sum(median_sum) < median_val:
            median_sum.append(ys[i])
            median_vals.append(i)
    
    median = xs[median_vals[-1]]
    
    fig,ax = plt.subplots()
    
    plt.plot([mean,mean],[0,max(ys)],'--',color='black',label='Mean')
    plt.plot([mode,mode],[0,max(ys)],'-.',color='black',label='Mode')
    plt.plot([median,median],[0,max(ys)],':',color='black',label='Median')
    
    ax.legend();
    
    for i in range(1,len(xs)):
        x_vals = [xs[i-1],xs[i]]
        y_vals = [ys[i-1],ys[i]]
        
        if xs[i] < (0.6 * max_hr):
            fill_color = 'blue'
        if xs[i] >= (0.6 * max_hr) and xs[i] < (0.7 * max_hr):
            fill_color = 'green'
        if xs[i] >= (0.7 * max_hr) and xs[i] < (0.8 * max_hr):
            fill_color = 'yellow'
        if xs[i] >= (0.8 * max_hr) and xs[i] < (0.9 * max_hr):
            fill_color = 'orange'
        if xs[i] >= (0.9 * max_hr):
            fill_color = 'red'
        
        if (ys[i-1] + ys[i]) != 0:    
            plt.plot(x_vals,y_vals,color=fill_color)
    
    #plt.plot(xs,ys)
        
    plt.xlabel("HR (bpm)")
    plt.ylabel('n')
    
    plt.ylim([0,max(ys)+5])
    plt.xlim([min(xs),max(xs)])

def hr_time_differential(df):
    hrs = df['HR'].tolist()
    times_un = df['time'].tolist()
    
    avg_hr = sum(hrs)/len(hrs)
    
    hr_diffs = []
    
    for i in range(0,len(hrs)):
        diff = hrs[i] - avg_hr
        hr_diffs.append(diff)
    
    times = []
    for i in range(0,len(times_un)):
        if i == 0:
            times.append(0)
        else:
            full_td = times_un[i] - times_un[0]
            full_secs = full_td.total_seconds()
            times.append(full_secs)
            
    plt.plot(times,hr_diffs)

def hr_delta(df):
    hrs = df['HR'].tolist()
    times_un = df['time'].tolist()
    
    times = []
    for i in range(0,len(times_un)):
        if i == 0:
            times.append(0)
        else:
            full_td = times_un[i] - times_un[0]
            full_secs = full_td.total_seconds()
            times.append(full_secs)
            
    deltas = [0]
    
    for i in range(1,len(hrs)):
        if i < 60:
            delta = hrs[i] - hrs[i-1]
        else:
            delta = (sum(hrs[i-30:i]) - sum(hrs[i-60:i-30]))/30
        
        deltas.append(delta)
        
    plt.plot(times,deltas)
    
def hr_html(df):
    hrs = df['HR'].tolist()
    
    mean = sum(hrs)/len(hrs)
    max_hr = max(hrs)
    min_hr = min(hrs)
    
    totals = []
    
    for i in range(0,len(hrs)):
        beats = hrs[i]/60
        totals.append(beats)
    
    total = sum(totals)
    
    xs = []
    ys = []
    
    for i in range(min_hr,max_hr+1):
        n = 0
        hr = i
        for v in range(0,len(hrs)):
            if hrs[v] == hr:
                n += 1
                
        xs.append(hr)
        ys.append(n)
    
    #mode_vals = [0]
    
    #for i in range(0,len(ys)):
    #    if ys[i] > mode_vals[-1]:
    #        mode_vals.append(i)
            
    #mode = xs[(mode_vals[-1])] - 1 
    
    mode_vals = []
    
    for i in range(0,len(ys)):
        if ys[i] == max(ys):
            mode_vals.append(i)
            
    mode = xs[mode_vals[0]]
    
    median_val = int(sum(ys)/2)
    median_sum = [ys[0]]
    median_vals = []
    
    for i in range(1,len(ys)):
        if sum(median_sum) < median_val:
            median_sum.append(ys[i])
            median_vals.append(i)
    
    median = xs[median_vals[-1]]
    
    html = f"""
<body>
<p>Average HR: {round(mean)} bpm<br>
Min. HR: {min_hr} bpm<br>
Max. HR: {max_hr} bpm<br>
Modal HR: {mode} bpm<br>
Median HR: {median} bpm<br>
Total number of heart beats: {round(total)} beats</p></body>"""    

    return(html)
               
#plt.show()    
#route = route_data('A8RG3448')
#print('Route pulled') 
#print(hr_html(route))
#plt.show()
#lap_bars(route)
#plt.show()
#hr_dist_durs_plot(route)
#plt.show()
#hr_zones_pie(route)
#plt.show()
#plt.show()
#hr_distribution(route)
#plt.show()
#hr_plot_time(route)