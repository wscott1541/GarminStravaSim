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
#import folium

from datetime import datetime

from . import data_read as dr
pull_data = dr.pull_data
dist_dict = dr.dist_dict
route_data = dr.route_data
activity_details = dr.activity_details

import matplotlib.pyplot as plt

from . import basic_functions as bf

#from analyse import route_data

import pandas as pd

import os

#import tilemapbase

import haversine

from bs4 import BeautifulSoup

import folium

def plot_osm_map(ac_df, width_input=75, height_input=75):
    
    output='map.html'
    #for i in range(len(speeds)):
    #    speeds[i] = speed_conversion(speeds[i])
    #speeds = speeds
    
    lat_min = ac_df['lat'].min()
    lon_min = ac_df['lon'].min()
    lat_max = ac_df['lat'].max() 
    lon_max = ac_df['lon'].max()
    
    lat_mean = ac_df['lat'].mean()#sum(lats)/len(lats)
    lon_mean = ac_df['lon'].mean()#sum(lons)/len(lons)
    
    dist_x = haversine.haversine((lat_mean,lon_min),(lat_mean,lon_max))
    dist_y = haversine.haversine((lat_min,lon_mean),(lat_max,lon_mean))
    
    ratio = dist_y/dist_x
    ###This method does not work because the inputs are relative to screen
    #height_input = int(round(width_input * ratio))
    
    m = folium.Map(location=[ac_df['lat'].mean(), ac_df['lon'].mean()],tiles = 'OpenStreetMap', width=f'{width_input}%',height=f'{height_input}%')
    
    lats = ac_df['lat'].tolist()
    lons = ac_df['lon'].tolist()
    points = []
    #ac_df['distance'] = ac_df['distance'].apply(lambda x: round(x/1000,1))
    #tt = ac_df['distance'].tolist()
    
    for i in range(0,len(lats)):
        #points = []
        p = tuple([lats[i],lons[i]])
        points.append(p)
        
        #folium.PolyLine(points, tooltip='{}'.format(tt[i]),color="red", weight=2.5, opacity=1).add_to(m)
    
    #ac_df['points'] = tuple([ac_df['lat'], ac_df['lon']])
    
    folium.PolyLine(points,color="red", weight=2.5, opacity=1).add_to(m)
    
    #HTML(m._repr_html_())
    
    sw = ac_df[['lat', 'lon']].min().values.tolist()
    ne = ac_df[['lat', 'lon']].max().values.tolist()

    m.fit_bounds([sw, ne])
    """
    m = folium.Map(location=[ac_df['lat'].mean(), ac_df['lon'].mean()],tiles = 'OpenStreetMap', width=f'{width_input}%',height=f'{height_input}%')

    lats = ac_df['lat'].tolist()
    lons = ac_df['lon'].tolist()
    dists = ac_df['distance'].tolist()
    
    for i in range(len(lats)):
        
        folium.CircleMarker(
            location=(lats[i], lons[i]),
            radius=1,#speeds[index]**2 / 8,
            tooltip=str(dists[i]),
            fill_color='red',
            fill=True,
            fill_opacity=1,
            weight=0,
        ).add_to(m)
    """
    
    m.save(output)
    
    with open(output) as fp:
        html = BeautifulSoup(fp, "html.parser")
        
    out = (str(html)[15:])
    
    os.remove(output)
    
    return (out)

def stretch_osm_map(ac_df, distance, width_input=75, height_input=75):
    
    output='map.html'
    
    m = folium.Map(location=[ac_df['lat'].mean(), ac_df['lon'].mean()],tiles = 'OpenStreetMap', width=f'{width_input}%',height=f'{height_input}%')
    
    for i in range(0,3):
        
        s_df = ac_df.loc[ac_df[distance] == i]
        
        lats = s_df['lat'].tolist()
        lons = s_df['lon'].tolist()
        points = []
    
        for n in range(0,len(lats)):
            p = tuple([lats[n],lons[n]])
            points.append(p)
    
    #ac_df['points'] = tuple([ac_df['lat'], ac_df['lon']])
    
        if i == 1:
            c = 'red'
        else:
            c = 'black'
    
        folium.PolyLine(points, color=c, weight=2.5, opacity=1).add_to(m)
    
    #HTML(m._repr_html_())
    
    sw = ac_df[['lat', 'lon']].min().values.tolist()
    ne = ac_df[['lat', 'lon']].max().values.tolist()

    m.fit_bounds([sw, ne])
    
    m.save(output)
    
    with open(output) as fp:
        html = BeautifulSoup(fp, "html.parser")
        
    out = (str(html)[15:])
    
    os.remove(output)
    
    return (out)


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
        if i < 5:
            speed = 0
        else:
            full_td = times_un[i] - times_un[i-5]
            full_secs = full_td.total_seconds()
            try:
                speed = (dists[i] - dists[i-5])/(full_secs) * 3.6
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
    
    #plt.gca().set_aspect('equal', adjustable='box')
    
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
    #plt.annotate('S',(lons[0],lats[0]),color='green')
    plt.scatter([lons[-1]],[lats[-1]],color='red')
    plt.annotate('{}km'.format(final),(lons[-1],lats[-1]),color='red')
    
    n = 1
    for i in range(0,len(dists)):
        if dists[i-1] < (n * 1000) and dists[i] > (n * 1000):
            plt.scatter([lons[i-1]],[lats[i-1]],color='grey')
            plt.annotate('{}km'.format(n),(lons[i-1],lats[i-1]),color='grey')
            n += 1
            
    plt.axis('off')
    
    plt.gca().set_aspect('equal', adjustable='box')
    
    #x_range = (max(lons) - min(lons))
    #y_range = (max(lats) - min(lats))
    
    #y_size = 4*(y_range)/(x_range)
    
    #fig_size = plt.rcParams["figure.figsize"]
    #fig_size[0] = 4
    #fig_size[1] = y_size
    #plt.rcParams["figure.figsize"] = fig_size

    
    #plt.axis('scaled')

#import data_read as dr

#last = dr.latest_activity('WS')
#ac_df = analyse.route_data(last)
#pyplot_basic(ac_df)    

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
    
    plt.gca().set_aspect('equal', adjustable='box')
    
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

def best_stretch_map(gpx_df,distance):
    times = gpx_df['time'].tolist()    
    distances = gpx_df['distance'].tolist()
    full = distances[-1]
    
    distance_times = []
    first = [0]
    ends = []
    
    if len(distances) > 0 and distance < full:
        for i in range(0,len(distances)):
            
            if distances[i] > distance - 1:
                if len(first) == 1:
                    first.append(i)
                
                for v in range(0,i):
                    if (distances[i] - distances[v-i]) > (distance - 1) and (distances[i] - distances[v-i]) < (distance + 100):
                        delta = times[i] - times[v-i]
                        distance_times.append(delta)
                        ends.append(distances[i])
    #print(distance_times)
    #print(ends)        
    endlist = []
    best_out = []
    
    if len(distance_times) > 0:
        #distance_times.sort()
        best = min(distance_times)
        best_out.append(best)
        #print(best)
        for i in range(0,len(distance_times)):
            if distance_times[i] == best:
                endlist.append(ends[i]) 
    
    end = endlist[0]
    #print(end)            
        
    lats = gpx_df['lat'].tolist()
    #print(lats[0])
    lons = gpx_df['lon'].tolist()
    
    #split_lons = []
    #split_lats = []
    
    #part_one_lons = []
    #part_one_lats = []
    
    #part_two_lons = []
    #part_two_lats = []
    
    #part = True
    
    for i in range(1,len(lats)):
        
        if distances[i] >= end - distance and distances[i] <= end:
            #split_lons.append(lons[i])
            #split_lats.append(lats[i])
            
            #part = False
            
            fill_color='red'
            dash = '-'
        #elif part == True:
            #part_one_lons.append(lons[i])
            #part_one_lats.append(lats[i])
            
            #fill_color='grey'
            #dash = ':'
            #split_lons.append(lons[i])
            #split_lats.append(lats[i])
        else:
            #part_two_lons.append(lons[i])
            #part_two_lats.append(lats[i])
            
            fill_color='grey'
            dash = ':'
            #split_lons.append(lons[i])
            #split_lats.append(lats[i])
        
        
        xs = [lons[i],lons[i-1]]
        ys = [lats[i],lats[i-1]]
        plt.plot(xs,ys,dash,color=fill_color)
    
    #plt.plot(part_one_lons,part_one_lats,':',color='grey')
    #plt.plot(split_lons,split_lats,color = 'red')
    #plt.plot(part_two_lons,part_two_lats,':',color='grey')
    
    plt.axis('off')
    
    plt.gca().set_aspect('equal', adjustable='box')
    
    #best_str = str(best_out[0])[-8:]
    
    #title = f'{distance}m: {best_str}'
    
    #plt.title(title)
    
    #matplotlib.axes.Axes.set_aspect(plt,'equal')
    
def best_stretch_map_c(ac_number,distance_word):
    gpx_df = route_data(ac_number,distance_word)
    #distance = dist_dict[distance_word]
    
    pre_section = gpx_df.loc[gpx_df[distance_word] == 0]
    section = gpx_df.loc[gpx_df[distance_word] == 1]
    post_section = gpx_df.loc[gpx_df[distance_word] == 2]
    
    plt.plot(pre_section['lon'],pre_section['lat'],':',color='grey')
    plt.plot(post_section['lon'],post_section['lat'],':',color='grey')
    plt.plot(section['lon'],section['lat'],color='red')
    
    plt.axis('off')
    
    plt.gca().set_aspect('equal', adjustable='box')
    
    #best_str = str(best_out[0])[-8:]
    
    #title = f'{distance}m: {best_str}'
    
    #plt.title(title)
    
    #matplotlib.axes.Axes.set_aspect(plt,'equal')
    
#best_stretch_map_c('B25C2227','1 mile')    

#ac_df = analyse.route_data('AAMC2600')
#best_stretch_map(ac_df,1600)

#from analyse import paul_df

#best_stretch_map(paul_df,1000) 


#print(cm.tab10[1])
#ac_df = analyse.route_data('A8FC1636')
#plt.show()
#pyplot_heatmap(ac_df)
#pyplot_colourmap(ac_df)
#pyplot_basic(ac_df)
#plt.show()
#plot_osm_map(output='test-speed-map.html', hr=None)


'''
import mplleaflet

def mplleaflet_test(activity_df):

    lons = activity_df['lon'].tolist()
    
    lats = activity_df['lat'].tolist()
    #print(lats[0])
    
    #print(lons[0])
    
    plt.plot(lons,lats)
    
    mplleaflet.show()
    
    mplleaflet.save_html()
    
import smopy

def smopy_test(activity_df):
    lats = activity_df['lat'].tolist()
    
    
    #print(lats[0])
    lons = activity_df['lon'].tolist()
    
    lat_min = min(lats)
    print(lat_min)
    lon_min = min(lons)
    print(lon_min)
    lat_max = max(lats)
    print(lat_max)
    lon_max = max(lons)
    print(lon_max)
    
    #map = smopy.Map((42., -1., 55., 3.), z=4)
    map = smopy.Map((lat_min,lon_min,lat_max,lon_max))
    
    #fig,ax = plt.subplots()
    
    #x, y = map.to_pixels(48.86151, 2.33474)
    ax = map.show_mpl(figsize=(8, 6))
    #ax.plot(x, y, 'or', ms=10, mew=2);
    ax.plot(lons, lats, color='blue')
    
    plt.savefig('check.png')
    
    #map.save_png('test.png')
    


def tmb_test(activity_df,plot_size = 'reg'):
    #lons = activity_df['lon'].tolist()
    #lats = activity_df['lat'].tolist()
    
    tilemapbase.start_logging()
    tilemapbase.init(create=True)
    t = tilemapbase.tiles.build_OSM()
    
    rang = 0.001
    
    #print(max(lats))
    
    lat_min = activity_df['lat'].min() - rang#min(lats) - rang
    #print(lat_min)
    lon_min = activity_df['lon'].min() - rang#min(lons) - rang
    #print(lon_min)
    lat_max = activity_df['lat'].max() + rang#max(lats) + rang
    #print(lat_max)
    lon_max = activity_df['lon'].max() + rang
    #print(lon_max)
    
    lat_mean = activity_df['lat'].mean()#sum(lats)/len(lats)
    lon_mean = activity_df['lon'].mean()#sum(lons)/len(lons)
    
    #delta_x = lon_max-lon_min
    #print(delta_x)
    #delta_y = lat_max-lat_min
    #print(delta_y)
    #plot_ratio=(delta_y)/(delta_x)
    
    dist_x = haversine.haversine((lat_mean,lon_min),(lat_mean,lon_max))
    dist_y = haversine.haversine((lat_min,lon_mean),(lat_max,lon_mean))
    
    #print(dist_x)
    #print(dist_y)
    
    plot_ratio = dist_x/dist_y
    #print(plot_ratio)
    #print(dist_ratio)
    
    #print(ratio)
    #ratio = dist_ratio
    
    extent = tilemapbase.Extent.from_lonlat(lon_min, lon_max,
                  lat_min, lat_max)
    #extent = extent.to_aspect(1.0)
    extent = extent.to_aspect(plot_ratio)
    
    path = [tilemapbase.project(x,y) for x,y in zip(activity_df['lon'],activity_df['lat'])]#zip(lons, lats)]
    x, y = zip(*path)
    
    if plot_size == 'reg':
        dimension = 10
    if plot_size == 'small':
        dimension = 4
    
    ratio = 1/plot_ratio
    
    fig, ax = plt.subplots(figsize=(dimension,ratio*dimension))

    plotter = tilemapbase.Plotter(extent, tilemapbase.tiles.build_OSM(), width=600)
    
    #if plot_size == 'reg':
    plotter.plot(ax)
    ax.plot(x, y)
    
    ax.set_xticks([lon_mean])#in some way, removes all the padding.
    ax.set_xticklabels(['-'])
    ax.set_yticks([lat_mean])
    ax.set_yticklabels(['1'])
    
        #plt.axis('off')
    ax.set_axis_off()
        
    #if plot_size == 'small':
    #    
    #    plotter.plot(plt.axes())#is the smaller map
    #    plt.plot(x,y)
    #    plt.axis('off')
    
    
    #ax.set_xlim([lon_min,lon_max])
    #ax.set_ylim([-90,90])
    
    #box = ax.get_position()
    #ax.set_position([box.x0-0.2, box.y0, box.width, box.height])
    
    #plotter.plot(plt.axes())#is the smaller map
    #plt.plot(x,y)
    
    #plt.axis('off')
    
    #plt.savefig('maybe.png',bbox_inches='tight')
    
    #fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
    #ax.xaxis.set_visible(False)
    #ax.yaxis.set_visible(False)

    #plotter = tilemapbase.Plotter(extent, t, width=600)
    #plotter.plot(ax, t)

    #x, y = tilemapbase.project(*my_office)
    #ax.plot(lons,lats, color="black", linewidth=20)
    
    #print(lats[0])
    
    
#ac_df = route_data('B25C2227')
#mplleaflet_test(ac_df)
#tmb_test(ac_df)
#plt.show()

'''

def average_route(user_df,activity):
    #types = user_df['Activity Type'].tolist()
    
    runs = ['ACRB1018','AB4H2007','AB3A3807','AAS92129','AA3D0046','AA3F3504']
    
    lengths = []
    
    for i in range(0,len(runs)):
        length = activity_details(user_df,runs[i],'Time')
        lengths.append(length)
        
    total_seconds = 55*60
    
    new_lat = []
    new_lon = []
    
    for s in range(0,total_seconds):
        new_lat.append([])
        new_lon.append([])
    
    for i in range(0,len(runs)):
        print(f'Assessing run {i}')
        
        route = route_data(runs[i])
        
        times = route['time'].tolist()
        lons = route['lon'].tolist()
        lats = route['lat'].tolist()
        
        for s in range(0,len(times)):
            pos = int((times[s] - times[0]).total_seconds())
            
            if pos < len(new_lat):
                new_lat[pos].append(lats[s])
                new_lon[pos].append(lons[s])
                
    avg_lats = []
    avg_lons = []
    
    print('Calculating averages')
    
    for i in range(0,len(new_lat)):
        if len(new_lat[i]) > 0:
            avg_lats.append(sum(new_lat[i])/len(new_lat[i]))
        if len(new_lon[i]) > 0:
            avg_lons.append(sum(new_lon[i])/len(new_lon[i]))
            
    avg_df = pd.DataFrame(columns=['lon','lat'])
    
    for i in range(0,len(avg_lats)):
        row = [avg_lons[i],avg_lats[i]]
        a_row = pd.Series(row,index=avg_df.columns)
        avg_df = avg_df.append(a_row,ignore_index=True)
        
    return(avg_df)

#ws_df = pull_data('WS')
#avg_route = average_route(ws_df,'Running')

#print(avg_route)

#tmb_test(avg_route)
#plt.savefig('avg_walk_test.jpg')

#pyplot_colourmap(ac_df)
        
    #plt.axis('off')
    
    #plt.gca().set_aspect('equal', adjustable='box')