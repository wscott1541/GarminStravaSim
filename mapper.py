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
    
def pyplot_heatmap(activity_df):
    #print(len(activity_number))
    df = activity_df#analyse.route_data(activity_number)
    
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
    
    mapper.set_array(virt_speeds)
    #plt.colorbar(mapper)
    cb = plt.colorbar(mapper)
    cb.set_label('Speed (km/h)')
    
    #one latitude/longtitude = 111km
    far_right = max(lons) + 0.0005
    #print('fr: ',far_right)
    top_up = max(lats) + 0.0005
    #print('top: ',top_up)
    fr_plus = far_right - (1/111)
    tu_plus = top_up - (1/111)
    arrow_x = [fr_plus,far_right,far_right]
    arrow_y = [top_up,top_up,tu_plus]
    plt.plot(arrow_x,arrow_y,color='grey',label='1km')
    
    #plt.scatter([lons[0]],[lats[0]],color='green')
    #plt.annotate('S',(lons[0],lats[0]),color='green')
    #plt.scatter([lons[-1]],[lats[-1]],color='red')
    #plt.annotate('F',(lons[-1],lats[-1]),color='red')
    
    #n = 1
    #for i in range(0,len(dists)):
    #    if dists[i-1] < (n * 1000) and dists[i] > (n * 1000):
    #        plt.annotate('{}km'.format(n),(lons[i-1],lats[i-1]))
    #        n += 1

def pyplot_basic(activity_df):
    df = activity_df#analyse.route_data(activity_number)
    
    lats = df['lat'].tolist()
    #print(lats[0])
    lons = df['lon'].tolist()
    #print(lons[0])
    dists = df['distance'].tolist()
    final = round(dists[-1]/1000,2)
    
    plt.plot(lons,lats)
    
    plt.scatter([lons[0]],[lats[0]],color='green')
    plt.annotate('S',(lons[0],lats[0]),color='green')
    plt.scatter([lons[-1]],[lats[-1]],color='red')
    plt.annotate('F: {}km'.format(final),(lons[-1],lats[-1]),color='red')
    
    n = 1
    for i in range(0,len(dists)):
        if dists[i-1] < (n * 1000) and dists[i] > (n * 1000):
            plt.scatter([lons[i-1]],[lats[i-1]],color='grey')
            plt.annotate('{}km'.format(n),(lons[i-1],lats[i-1]),color='grey')
            n += 1
            
    plt.axis('off')

def pyplot_colourmap(activity_df):
    #print(len(activity_number))
    #df = activity_df#analyse.route_data(activity_number)
    
    #print(len(times_un))

    lats = activity_df['lat'].tolist()
    #print(lats[0])
    lons = activity_df['lon'].tolist()
    #print(lons[0])
    dists = activity_df['distance'].tolist()

    n = 1
    markers = [0]
    
    for i in range(0,len(dists)):
        
        if dists[i-1] < (n * 1000) and dists[i] > (n * 1000):
            markers.append(i-1)
            
            n += 1
    markers.append(len(dists))
    #colors = ['red','blue','green'] 
    #norm = matplotlib.colors.Normalize(vmin=0, vmax=len(markers), clip=True)
    #mapper = cm.ScalarMappable(norm=norm, cmap=cm.tab20)
    
    #color_options = ['black']
    
    for i in range(1,len(markers)):
        sta = markers[i-1]
        fin = markers[i]
        minor_lats = []
        minor_lons = []
        for v in range(0,len(lats)):
            if v >= sta and v <= fin:
                minor_lats.append(lats[v])
                minor_lons.append(lons[v])
        #fill_color=matplotlib.colors.to_hex(mapper.to_rgba(i))
        plt.plot(minor_lons,minor_lats)
    plt.axis('off')
    """
    plt.axis('off')
    #one latitude/longtitude = 111km
    far_right = max(lons) + 0.0005
    #print('fr: ',far_right)
    top_up = max(lats) + 0.0005
    #print('top: ',top_up)
    fr_plus = far_right - (1/111)
    tu_plus = top_up - (1/111)
    arrow_x = [fr_plus,far_right,far_right]
    arrow_y = [top_up,top_up,tu_plus]
    plt.plot(arrow_x,arrow_y,color='blue',label='1km')
    
    plt.scatter([lons[0]],[lats[0]],color='green')
    plt.annotate('S',(lons[0],lats[0]),color='green')
    plt.scatter([lons[-1]],[lats[-1]],color='red')
    plt.annotate('F',(lons[-1],lats[-1]),color='red')
    
    n = 1
    for i in range(0,len(dists)):
        if dists[i-1] < (n * 1000) and dists[i] > (n * 1000):
            plt.annotate('{}km'.format(n),(lons[i-1],lats[i-1]))
            n += 1
    """

#print(cm.tab10[1])
ac_df = analyse.route_data('A8CK1828')
plt.show()
pyplot_heatmap(ac_df)
#pyplot_colourmap(ac_df)
#pyplot_basic(ac_df)
plt.show()
#plot_osm_map(output='test-speed-map.html', hr=None)