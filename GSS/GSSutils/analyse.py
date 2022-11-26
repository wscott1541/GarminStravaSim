#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 14:18:22 2020

@author: WS
"""

#column reference: ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status']

from . import data_read as dr
from . import basic_functions as bf

import pandas as pd
from datetime import datetime, timedelta

from time import time

import os

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
#pio.to_html(fig,auto_play=False,full_html=False)

#import primary_user_functions as puf
#from . import primary_user_functions as puf 
from . import basic_functions as bf
minutes_axes_label = bf.minutes_axes_label

def remove_padding(t):
    if t[0] == '0':
        t = t[1]
    return(t)
 
import matplotlib.pyplot as plt

def limit_pace(x):
    if x > 12:
        x = 12
    return()

def distance_pace(df):
    
    df['time'] = df['time'].apply(bf.convert_time)
    df['td'] = df['time'] - df.iloc[0]['time']
    df['minutes'] = df['td'].apply(lambda x: x.total_seconds())
    df['minutes'] = df['minutes'].apply(lambda x: x/60)
    df['delta_min'] = df['minutes'].diff(periods=15)
    
    df['km'] = df['distance'] / 1000
    
    df['delta_km'] = df['km'].diff(periods=15)
    
    df['pace'] = (df['delta_min'] / df['delta_km']).rolling(30).mean()
    
    #mean = (df['pace'].mean())
    #std = (df['pace'].std())
    
    #print(df)
    
    #df = df.loc[df['pace'] < mean+std]
    
    #print(type(df['pace'][16]))
    
    #df['pace'] = df['pace'].apply(limit_pace)
    
    df['pace'] = df['pace'].apply(lambda x: 1/x)
    
    fig,ax = plt.subplots()
    
    plt.plot(df['km'],df['pace'])
    
    locs, labels = plt.yticks() 
    
    ticks = []
    labels = []
    
    for i in range(2,len(locs)):
        tick = locs[i]
        label = round(1/locs[i],2)
        ticks.append(tick)
        labels.append(label)
    
    plt.yticks(ticks,labels)
    
    #print(locs)
    #print(labels)
    
    ax.set_ylabel('Pace (min/km)')
    ax.set_xlabel('Distance (km)')

def pace_alt_distance_plotly(df):
    
    try:
        df['check'] = df['alt'].apply(lambda x: int(x))
        
        #calculate alt
        df['alt'] = df['alt'].apply(lambda x: round(x,1))#also breaks nan
        df['alt'] = df['alt'].rolling(30,min_periods=1).mean()
        #df['alt'] = df['alt'].apply(lambda x: round(x,1))    
    
        #calculate pace
        df['time'] = df['time'].apply(bf.convert_time)
        df['td'] = df['time'] - df.iloc[0]['time']
        df['minutes'] = df['td'].apply(lambda x: x.total_seconds())
        df['minutes'] = df['minutes'].apply(lambda x: x/60)
        df['delta_min'] = df['minutes'].diff(periods=3)
        df['km'] = df['distance'] / 1000
        df['delta_km'] = df['km'].diff(periods=3)
        
        df['pace'] = (df['delta_min'] / df['delta_km']).rolling(15).mean()

        df['pace'] = df['pace'].apply(lambda x: 1/x)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        #ALT
        #fig.add_trace(
        #    go.Scatter(x=df['distance'], y=df['alt'], name="Height", fill='tozeroy')
        #    secondary_y=False, 
        #    )        
        
        fig.add_trace(
            go.Scatter(x=df['distance'], 
                       y=df['alt'], 
                       name="Height",
                       fill='tozeroy'),
            secondary_y=False,
            )
        
        if df['alt'].max() < 75 and df['alt'].min() > 0:
            fig.update_layout(
                yaxis=dict(
                    range=[0, 75]
                    ))
        elif df['alt'].max() < 75 and df['alt'].min() < 0:
            fig.update_layout(
                yaxis=dict(
                    range=[df['alt'].min() - 3, 75]
                    ))
        elif df['alt'].max() > 75 and df['alt'].min() > 0:
            fig.update_layout(
                yaxis=dict(
                    range=[0, df['alt'].max()+3]
                    ))
        elif df['alt'].max() > 75 and df['alt'].min() < 0:
            fig.update_layout(
                yaxis=dict(
                    range=[df['alt'].min() - 3, df['alt'].max()+3]
                    ))

        #print('trace 1')

        fig.add_trace(
            go.Scatter(x=df['distance'], 
                       y=df['pace'], 
                       name="Pace (misc. units)"),
            secondary_y=True,
            )
        
        
        
        div = pio.to_html(fig,auto_play=False,full_html=False)
        
    except:
        
        df['time'] = df['time'].apply(bf.convert_time)
        df['td'] = df['time'] - df.iloc[0]['time']
        df['minutes'] = df['td'].apply(lambda x: x.total_seconds())
        df['minutes'] = df['minutes'].apply(lambda x: x/60)
        df['delta_min'] = df['minutes'].diff(periods=15)
        df['km'] = df['distance'] / 1000
        df['delta_km'] = df['km'].diff(periods=15)
        df['pace'] = (df['delta_min'] / df['delta_km']).rolling(30).mean()
        df['pace'] = df['pace'].apply(lambda x: 1/x)
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(x=df['distance'], 
                       y=df['pace'], 
                       name="Pace (misc. units)")
            )
        
        div = pio.to_html(fig,auto_play=False,full_html=False)
        
        div = div + '<p>Altitudes not found</p>'
    
    return(div)

def distance_plotly(df):
    #define the available information
    try:
        df['check'] = df['alt'].apply(lambda x: int(x))
        alts = True
    except:
        alts = False
        
    try:
        df['check'] = df['HR'].apply(lambda x: int(x))
        hr = True
    except:
        hr = False
        
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    #calculate pace
    df['time'] = df['time'].apply(bf.convert_time)
    df['td'] = df['time'] - df.iloc[0]['time']
    df['minutes'] = df['td'].apply(lambda x: x.total_seconds())
    df['minutes'] = df['minutes'].apply(lambda x: x/60)
    df['delta_min'] = df['minutes'].diff(periods=30)#.fillna(0)
    df['delta_min'] = df.apply(lambda row: row['delta_min'] if row['delta_min'] == row['delta_min'] else row['minutes'],axis=1)
    
    df['km'] = df['distance'] / 1000
    df['delta_km'] = df['km'].diff(periods=30)#.fillna(0)
    df['delta_km'] = df.apply(lambda row: row['delta_km'] if row['delta_km'] == row['delta_km'] else row['km'],axis=1)
        
    df['pace'] = (df['delta_min'] / df['delta_km']).rolling(45,min_periods=1).mean()
    
    df['pace_annot'] = df['pace'].fillna(0).apply(bf.cropped_floatminute_to_stringtime)
    df['pace'] = df['pace'].apply(lambda x: 1/x if x != 0 else 0.05)
    df['pace'] = df['pace'].apply(lambda x: 0.05 if x < 0.05 else x)
        
    df['time_annot'] = df['td'].apply(lambda x: datetime.strptime(str(x)[7:],'%H:%M:%S'))
    df['time_annot'] = df['time_annot'].apply(lambda x: datetime.strftime(x,'%M:%S') if datetime.strftime(x,'%H') == '00' else datetime.strftime(x,'%H:%M:%S'))
    
    hover_t = '''Distance: %{x}m
<br>Time: %{customdata[0]}
<br>Pace: %{customdata[1]}/km<extra></extra>'''
    
    fig.add_trace(
            go.Scatter(x=df['distance'], 
                       y=df['pace'], 
                       name="Pace (misc. units)",
                       customdata = df[['time_annot','pace_annot']],
                       hovertemplate = hover_t),
            secondary_y=True,
            )
    
    if alts == True:
        df['alt'] = df['alt'].apply(lambda x: round(x,1))#also breaks nan
        df['alt'] = df['alt'].rolling(30,min_periods=1).mean()
        #df['alt'] = df['alt'].apply(lambda x: round(x,1))    

        df['alt_annot'] = df['alt'].apply(lambda x: round(x))

        hover_t = '''Distance: %{x}m
<br>Time: %{customdata[0]}
<br>Elevation: %{customdata[1]}m<extra></extra>'''

        fig.add_trace(
            go.Scatter(x=df['distance'], 
                   y=df['alt'], 
                   name="Elevation",
                   fill='tozeroy',
                   customdata = df[['time_annot','alt_annot']],
                   hovertemplate = hover_t),
            secondary_y=False,
            )
        
        if df['alt'].max() < 150 and df['alt'].min() > 0:
            fig.update_layout(
                yaxis=dict(
                    range=[0, 150]
                    ))
        elif df['alt'].max() < 150 and df['alt'].min() < 0:
            fig.update_layout(
                yaxis=dict(
                    range=[df['alt'].min() - 3, 150]
                    ))
        elif df['alt'].max() > 150 and df['alt'].min() > 0:
            fig.update_layout(
                yaxis=dict(
                    range=[0, df['alt'].max()*1.1]
                    ))
        elif df['alt'].max() > 150 and df['alt'].min() < 0:
            fig.update_layout(
                yaxis=dict(
                    range=[df['alt'].min() - 3, df['alt'].max()*1.1]
                    ))
    
    if hr == True:
        #if alts == True:
        #    sec_y_hr =False
        #    hr_vis = 'legendonly'
            
        max_bound = df['pace'].max() * 0.8

        max_hr = df['HR'].max()
        
        df['hr_plot'] = (df['HR']/max_hr) * max_bound
        df['hr_plot'] = df['hr_plot'].rolling(30,min_periods=1).mean()
        df['hr_annot'] = (df['hr_plot'] * max_hr)/max_bound
        df['hr_annot'] = df['hr_annot'].apply(lambda x: 'HR: ' + str(round(x)))
        df['annot'] = 'Time: ' + str(df['time']) + '''
HR: ''' + str(df['hr_annot'])   
        df['t_annot'] = df['time'].apply(lambda x: 'Time: ' + str(x))
        df['annot'] = df['t_annot'] + '''
        
''' + df['hr_annot']

        
        hover_t = '''Distance: %{x}m
<br>%{customdata[0]}
<br>%{customdata[1]}<extra></extra>'''

        #text_template = ['''Time: {}, {}'''.format(a,b) for a and b in df['time'].tolist() and df['hr_annot'].tolist()]
        
        fig.add_trace(
            go.Scatter(x=df['distance'], 
                       y=df['hr_plot'], 
                       name="HR",
                       customdata = df[['t_annot','hr_annot']],
                       hovertemplate = hover_t),
                       #text = df['annot']),#df['hr_annot']),
                       
                secondary_y=True,
                )#visible='legendonly'),
         
    div = pio.to_html(fig,auto_play=False,full_html=False)        
    
    return(div)

    

def hr_plot_time(df):

    try:
        times_un = df['time'].tolist()
        hrs = df['HR'].tolist()
    except:
        new = dr.route_data(df)
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
        new = dr.route_data(df)
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
    
def assign_zones(x):
    max_hr = 220 - 26
    
    if x < max_hr * 0.6:
        z = 1
    if x >= max_hr * 0.6 and x < max_hr * 0.7:
        z = 2
    if x >= max_hr * 0.7 and x < max_hr * 0.8:
        z = 3
    if x >= max_hr * 0.8 and x < max_hr * 0.9:
        z = 4
    if x >= max_hr * 0.9:
        z = 5
    
    return(z)

def hr_zones_pie_plotly(df):
    #assumes equal timestep    
    df['zone'] = df['HR'].apply(assign_zones)
    
    zones = {}
    
    for i in range(1,6):
        zones[f'{i}'] = len(df[df['zone'] == i])
        
    t = df.iloc[-1]['time'] - df.iloc[0]['time']
    t = str(t)[-8:]
    #t = datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
    #t = datetime.strftime(t,'%H:%M:%S')
    t = bf.stringtime_to_floatminute(t)
    
    labels = {}
    
    for i in range(1,6):
        rel_t = (zones[f'{i}']/len(df)) * t #sum(zones.values())
        labels[f'{i}'] = f'Zone {i}: ' + bf.cropped_floatminute_to_stringtime(rel_t)
        #labels[f'{i}'] = rel_t
        
    #raise ValueError(t)
    
    pie_colors = ['#B6E880','#EECA3B','#FF9900','#E45756','#D62728']
    
    fig = go.Figure(
        data=
        [go.Pie(
            labels=list(labels.values()), values=list(zones.values()),
            direction ='clockwise',
            marker_colors=pie_colors,
            sort=False)])
    
    div = pio.to_html(fig,auto_play=False,full_html=False)   
    
    return(div)
    
    
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
        if i < len(markers)-1:
            label = f'{i-1}-{i}km'
        else:
            fin = round((dists[-1]/1000),2)
            #print(fin)
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
    
    #print(order)
    #print(lap_times)
    
    for i in range(0,len(order)):
        if lap_times[i] > 2:
            pos = 0.4 * lap_times[i]
        else:
            pos = lap_times[i] + 0.1
        
        mins = int(lap_times[i])
        secs = round(60*(lap_times[i]-mins))
        
        t_text = f'{mins}m{secs}'
        
        plt.text(pos,order[i]-0.1,t_text)
    
    #for i in range(0,len(lap_times)):
    #    plt.text()
    #for index, value in enumerate(lap_times):
    #    plt.text(value, index+1, str(value))

#print('Starting')    
#route = route_data('AABB0534')
#print('Route pulled')
#lap_bars(route)    

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

def metres_per_beat(df):
    dists = df['distance'].tolist()
    hrs = df['HR'].tolist()
    times_un = df['time'].tolist()
    
    mpbs = [0]
    
    for i in range(1,len(dists)):
        metres = dists[i] - dists[i-1]
        t_d =  times_un[i] - times_un[i-1]
        t_d_s = t_d.total_seconds()
        beats = (t_d_s*(hrs[i]+hrs[i-1]))/(2*60)
        mpb = metres/beats
        mpbs.append(mpb)
        
    plt.plot(dists,mpbs)

def pace(user_df,ac_no):
    
    dur = dr.activity_details(user_df,ac_no,'Duration')
    dist = dr.activity_details(user_df,ac_no,'Distance')
    
    hours = float(dur[:2])
    
    mins = 60 * hours + float(dur[3:5]) + (float(dur[-2:])/60)
    
    pace = mins / dist
    
    pace_mins = int(pace)
    pace_secs = round(60*(pace-pace_mins))
        
    text = f'{pace_mins}m{pace_secs}'
    
    return(text)
    
def dist_dur_comp(df):
    dists = df['distance'].tolist()
    dur = df['time'].tolist()
    
    minutes = []
    times = []
    for i in range(0,len(dur)):
        if i == 0:
            times.append(0)
            minutes.append(0)
        else:
            full_td = dur[i] - dur[0]
            full_secs = full_td.total_seconds()
            times.append(full_secs)
            full_mins = full_secs/60
            minutes.append(full_mins)

    #print(minutes[-1])    
    
    #fiojg = fgkje    
    
    difference = [0]
    
    for i in range(1,len(dur)):
        delta = (dists[i] - times[i]) - (dists[i-1] - times[i-1])
        difference.append(delta)
    
    fig,ax = plt.subplots() 
        
    plt.plot([0,times[-1]],[0,dists[-1]],color='grey')
    
    for i in range(1,len(dur)):
        #print(i,'/',len(dur)-1)
        xs = [times[i-1],times[i]]
        ys = [dists[i-1],dists[i]]
        
        if difference[i] >= 0:
            colour = 'green'
        else:
            colour = 'red'
            
        plt.plot(xs,ys,color=colour)
        
    tags,points = minutes_axes_label(minutes)
    
    new_points = []
    for i in range(0,len(points)):
        new_point = points[i] * 60
        new_points.append(new_point)
    
    ax.set_xticks(new_points)
    ax.set_xticklabels(tags)
    
    ax.set_xlabel('Duration')
    
    ax.set_ylabel('Distance (m)')
    
    
        
def dur_dist_comp(df):
    dists = df['distance'].tolist()
    dur = df['time'].tolist()
    
    times = []
    for i in range(0,len(dur)):
        if i == 0:
            times.append(0)
        else:
            full_td = dur[i] - dur[0]
            full_secs = full_td.total_seconds()
            times.append(full_secs)
            
    difference = [0]
    
    for i in range(1,len(dur)):
        delta = (times[i] - dists[i]) - (times[i-1] - dists[i-1])
        difference.append(delta)
            
    plt.plot([0,dists[-1]],[0,times[-1]],color='grey')
    
    for i in range(1,len(dur)):
        xs = [dists[i-1],dists[i]]
        ys = [times[i-1],times[i]]
        
        
        if difference[i] >= 0:
            colour = 'red'
        else:
            colour = 'green'
            
        plt.plot(xs,ys,color=colour)
        
def prep_interval_df(df:pd.DataFrame, distance:str)->pd.DataFrame:
    
    dist_cols = {k.replace(' ',''):k for k in dr.dist_dict}
    dist_col = dist_cols[distance]
        
    df = df[df[dist_col]==1]#Keep only the times relevant to the split
    df = df.reset_index(drop=True)

    df['distance_cut'] = df['distance'].diff().fillna(0)
    df['distance_cut'] = df['distance_cut'].cumsum()
    
    return df
    
        
def km_splits_bars_plotly(df: pd.DataFrame, distance:str=None, whole_activity:bool=True)->str:
    #dr.dist_dict
    
    non_km_splits = {
        '1km': 500,
        '1mile': dr.dist_dict['1 mile']/4,
        '1.5mile': dr.dist_dict['1.5 mile']/3,
        '3mile': dr.dist_dict['3 mile']/3
        }
    
    if not whole_activity:
        df = prep_interval_df(df, distance)
        #dist_cols = {k.replace(' ',''):k for k in dr.dist_dict}
        #dist_col = dist_cols[distance]
        
        #df = df[df[dist_col]==1]#Keep only the times relevant to the split
        #df = df.reset_index(drop=True)

        #df['distance_cut'] = df['distance'].diff().fillna(0)
        #df['distance_cut'] = df['distance_cut'].cumsum()
        
        #raise ValueError(df[['distance','distance_cut']].head())
    else:
        df['distance_cut'] = df['distance']
    
    interval_distance = non_km_splits[distance] if distance and distance in non_km_splits  else 1000
    #raise ValueError(interval_distance)
    
    df['interval'] = df['distance_cut'].apply(lambda x: x // interval_distance)#convert to km, assign each
    
    #raise ValueError(df['distance_cut'][:25])
    
    splits = {}
    
    for k in df['interval'].unique():
        start_time = df[df['interval']==k]['time'].min()
        end_time = df[df['interval']==k]['time'].max()
        
        split_time = end_time - start_time 
        
        split_seconds = split_time.total_seconds()
        
        start_dist = df[df['interval']==k]['distance_cut'].min()
        end_dist = df[df['interval']==k]['distance_cut'].max()
        
        start_dist = round(start_dist/1000,2)
        end_dist = round(end_dist/1000,2)
        
        split_dist = f'{start_dist}km-{end_dist}km'
        
        if end_dist - start_dist > 25/1000:
            splits[split_dist] = split_seconds
        
        #raise ValueError(splits)
        
    #raise ValueError(splits)
    
    bars = list(splits.keys())
    heights = list(splits.values())
    labels = [bf.seconds_to_str_minutes(t) for t in heights]
    
    #raise ValueError(labels)
    
        
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=bars, 
            y=heights,
            text=labels,
            textposition='auto'
            )
        )
    
    div = pio.to_html(fig,auto_play=False,full_html=False)
    
    return div
        
        
def halfway_split_str(df:pd.DataFrame, distance:str)->(str, str, str):
    
    dist_cols = {k.replace(' ',''):k for k in dr.dist_dict}
    dist_col = dist_cols[distance]
        
    #df = df[df[dist_col]==1].reset_index(drop=True)#Keep only the times relevant to the split
    
    #df['distance_cut'] = df['distance'].diff().fillna(0)
    #df['distance_cut'] = df['distance_cut'].cumsum()
    
    df = prep_interval_df(df, distance)
    
    halfway = dr.dist_dict[dist_col]/2
    
    df['interval'] = df['distance_cut'].apply(lambda x: 'front' if x // halfway == 0 else 'back')
    
    splits = {}
    
    for i in ('front', 'back'):
        start_time = df[df['interval']==i]['time'].min()
        end_time = df[df['interval']==i]['time'].max()

        split_time = end_time - start_time 
        
        split_seconds = split_time.total_seconds()   
        
        splits[i] = split_seconds

    front = bf.seconds_to_str_minutes(splits['front'])    
    back = bf.seconds_to_str_minutes(splits['back'])    
        
    diff = splits['back'] - splits['front']
    diff = bf.seconds_to_str_minutes(diff)
    
    return front, back, diff

def calc_reigel_time(current_best_time, distance_run, distance_to_run):
    # T2 = T1 x (D2/D1) 1.06
    
    D1 = dr.dist_dict[distance_run]
    D2 = dr.dist_dict[distance_to_run]
    
    current_best_time = bf.split_to_dt(current_best_time)
    start = datetime.strptime('00:00:00', '%H:%M:%S')
    current_best_time = current_best_time - start
    current_best_time = current_best_time.total_seconds()
    
    projected_best_time = current_best_time * ((D2/D1) ** 1.06)
    
    #raise ValueError(projected_best_time, D1, D2)
    
    return projected_best_time#bf.seconds_to_str_minutes(projected_best_time)
    
    
def distance_reigel_efficiency(user_df: pd.DataFrame, ac_no: str, distance: str)->str:
    
    # https://www.runnersworld.com/uk/training/a761681/rws-race-time-predictor/#:~:text=It's%20based%20on%20a%20formula,the%20calculated%20time%20for%20D2.
    # https://www.ukresults.net/misc/predictor.html

    if distance in ['1km', '1mile']:
        return ''
    else:
        dtag = bf.durl_to_dtag(distance)
        
        time_run = dr.ac_detail(ac_no, dtag)
        
        distances = list(dr.dist_dict.keys())
        
        distances = [d for d in distances if dr.dist_dict[d] < dr.dist_dict[dtag] and d != '1km']
        #comp_dist = None
        
        #for n, d in enumerate(distances[1:]):
        #    if distance == 'Half':
        #        comp_dist = '10km'
        #    elif d == distance and not comp_dist:
        #        comp_dist = distances[n-1]
        #        #i.e. compare with 1km for a mile, 5km for 5 miles, but not 20km for half (10km favoured)
        
        date = dr.ac_detail(ac_no, 'Date')
        
        user_df = user_df[user_df['Date'] < date]#keep only preceding PBs
        
        def fetch_pb(dtag_col: str)->str:
            return user_df[dtag_col].min()
        
        pbs = {d: fetch_pb(d) for d in distances}
        
        projected_times = {d: calc_reigel_time(pbs[d], d, dtag) for d in distances}
        
        #raise ValueError(projected_times)
        
        best_projection = None
        projected_from = None
        projection_source = None
        
        for d, t in projected_times.items():
            #t_seconds = bf.split_to_dt(t)
            #start = datetime.strptime('00:00:00', '%H:%M:%S')
            #t_seconds = t_seconds - start
            #t_seconds = t_seconds.total_seconds()
            if best_projection is None or t < best_projection:
                best_projection = t
                projected_from = d
                projection_source = pbs[d]
                
        return f'''A {time_run.replace('0 days ','')} {dtag}
compares with a projected best time of {str(timedelta(seconds=best_projection))[:-str(timedelta(seconds=best_projection)).rfind('.')]},
calculated from a {projected_from} PB of {projection_source.replace('0 days ','')}'''
