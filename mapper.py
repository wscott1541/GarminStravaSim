#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 15:32:47 2020

@author: WS

https://github.com/bunnie/watchmap/blob/master/plot.py
https://www.earthdatascience.org/courses/scientists-guide-to-plotting-data-in-python/plot-spatial-data/customize-raster-plots/interactive-maps/
"""

import matplotlib
import matplotlib.cm as cm
import folium

from datetime import datetime

import pandas as pd

import os
"""
abbr_data = pd.read_csv(r'temp-abbr.csv')
abbr_df = pd.DataFrame(abbr_data,columns=['Abbr'])
abbrs = abbr_df['Abbr'].tolist()

ac_abbr = abbrs[0]

fileDir = os.path.dirname(os.path.realpath('__file__'))

filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.csv'.format(ac_abbr))

data = pd.read_csv(filename)

csv_df = pd.DataFrame(data,columns=['time','lat','lon','distance'])

times_strings = csv_df['time'].tolist()
times_un = []
for i in range(0,len(times_strings)):
    time_obj = datetime.strptime(times_strings[i],'%Y-%m-%d %H:%M:%S')
    times_un.append(time_obj)

lats = csv_df['lat'].tolist()
lons = csv_df['lon'].tolist()
dists = csv_df['distance'].tolist()

times = []
speeds = []
sorted_speeds = []

for i in range(0,len(times_un)):
    time = times_un[i] - times_un[0]
    if i == 0:
        speed = 0
    else:
        full_td = times_un[i] - times_un[i-1]
        full_secs = full_td.total_seconds()
        try:
            speed = (dists[i] - dists[i-1])/(full_secs)
        except:
            speed = 0
    times.append(time)
    speeds.append(speed)
    sorted_speeds.append(speed)

sorted_speeds.sort()
"""
"""
def plot_osm_map(output='speed-map.html', hr=None):
    #for i in range(len(speeds)):
    #    speeds[i] = speed_conversion(speeds[i])
    #speeds = speeds
    minima = min(speeds)
    maxima = max(speeds)

    norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.plasma)
    m = folium.Map(location=[lats[0], lons[0]],tiles = 'OpenStreetMap', zoom_start=15)
    for index in range(len(lats)):
        if speeds[index] == 0:
            speeds[index] = 0.01

        if hr:
            try:
                tooltip="{:0.1f}kph".format(speeds[index]) + ' ' + str(hr['hr'][index]) +'bpm'
            except:
                tooltip="{:0.1f}kph".format(speeds[index])
        else:
            tooltip=str(speeds[index])
        folium.CircleMarker(
            location=(lats[index], lons[index]),
            radius=0.5,#speeds[index]**2 / 8,
            tooltip=tooltip,
            fill_color=matplotlib.colors.to_hex(mapper.to_rgba(speeds[index])),
            fill=True,
            fill_opacity=0.2,
            weight=0,
        ).add_to(m)
    
    #HTML(m._repr_html_())
    
    m.save(output)
    
def osm_map_to_email(hr=None):
    #for i in range(len(speeds)):
    #    speeds[i] = speed_conversion(speeds[i])
    #speeds = speeds
    minima = min(speeds)
    maxima = max(speeds)

    norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.plasma)
    m = folium.Map(location=[lats[0], lons[0]],tiles = 'OpenStreetMap', zoom_start=15)
    for index in range(len(lats)):
        if speeds[index] == 0:
            speeds[index] = 0.01

        if hr:
            try:
                tooltip="{:0.1f}kph".format(speeds[index]) + ' ' + str(hr['hr'][index]) +'bpm'
            except:
                tooltip="{:0.1f}kph".format(speeds[index])
        else:
            tooltip=str(speeds[index])
        folium.CircleMarker(
            location=(lats[index], lons[index]),
            radius=0.5,#speeds[index]**2 / 8,
            tooltip=tooltip,
            fill_color=matplotlib.colors.to_hex(mapper.to_rgba(speeds[index])),
            fill=True,
            fill_opacity=0.2,
            weight=0,
        ).add_to(m)
    
    #HTML(m._repr_html_())
    
    return(m)
"""
import matplotlib.pyplot as plt

import analyse
    
def pyplot_map(activity_number):
    #print(len(activity_number))
    df = analyse.route_data(activity_number)
    
    times_un = df['time'].tolist()
    #times_un = []
    #for i in range(0,len(times_strings)):
    #    time_obj = datetime.strptime(times_strings[i],'%Y-%m-%d %H:%M:%S')
    #    times_un.append(time_obj)

    #print(len(times_un))

    lats = df['lat'].tolist()
    #print(lats[0])
    lons = df['lon'].tolist()
    #print(lons[0])
    dists = df['distance'].tolist()

    times = []
    speeds = []
    sorted_speeds = []

    for i in range(0,len(times_un)):
        time = times_un[i] - times_un[0]
        if i == 0:
            speed = 0
        else:
            full_td = times_un[i] - times_un[i-1]
            full_secs = full_td.total_seconds()
            try:
                speed = (dists[i] - dists[i-1])/(full_secs)
            except:
                speed = 0
        times.append(time)
        speeds.append(speed)
        sorted_speeds.append(speed)

    sorted_speeds.sort()
    
    #minima = min(speeds)
    #maxima = max(speeds)
    lower_n = round(len(speeds) * 0.03)
    #print(lower_n)
    #print(speeds[lower_n])
    upper_n = round(len(speeds) * 0.98)
    lower = sorted_speeds[lower_n]#[0]
    upper = sorted_speeds[upper_n]#[-1]
    virt_speeds = []
    for i in range(0,len(speeds)):
        if speeds[i] < lower:
            temp_speed = lower
        elif speeds[i] > upper:
            temp_speed = upper
        else:
            temp_speed = speeds[i]
        virt_speeds.append(temp_speed)

    norm = matplotlib.colors.Normalize(vmin=lower, vmax=upper, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.plasma)
    #cm.plasma
    
    for i in range(1,len(lats)):
        fill_color=matplotlib.colors.to_hex(mapper.to_rgba(virt_speeds[i]))
        xs = [lons[i],lons[i-1]]
        ys = [lats[i],lats[i-1]]
        plt.plot(xs,ys,color=fill_color)
    plt.axis('off')
    #one latitude/longtitude = 111km
    far_right = max(lons)
    #print('fr: ',far_right)
    top_up = max(lats)
    #print('top: ',top_up)
    fr_plus = far_right - (1/111)
    tu_plus = top_up - (1/111)
    arrow_x = [fr_plus,far_right,far_right]
    arrow_y = [top_up,top_up,tu_plus]
    plt.plot(arrow_x,arrow_y,color='blue',label='1km')

#plt.show()
#pyplot_map('A85I1222')
#plt.show()
#plot_osm_map(output='test-speed-map.html', hr=None)