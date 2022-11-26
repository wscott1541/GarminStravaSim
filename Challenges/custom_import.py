#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Move this to Challenges, alongside custom_route or the first gpx file
Amend FIRST_FILE, FIRST_PLACE, NEXT_PLACE as appropriate

Run in command line
"""

import gpxpy
import haversine
import numpy as np
import pandas as pd

from datetime import datetime
from math import sqrt

#set-up only
FIRST_FILE = 'Starting_Route.gpx'
FIRST_PLACE = 'Starting Point'

#following additions.  Once at a time, please.
NEXT_PLACE = 'Next Place'

if NEXT_PLACE == 'Next Place':
    raise ValueError('NEXT_PLACE needs replacing')

def import_data(file_name):
    try:
        gpx_file = open(file_name)
        gpx_unpacked = gpxpy.parse(gpx_file)

        data = gpx_unpacked.tracks[0].segments[0].points
        
        stop = 0
    except:
        stop = 1
        raise ValueError('Early break')

    return data

def load_data(df,data):
    for i in range(0,len(data)):
        lon = data[i].longitude
        lat = data[i].latitude
                
        a_row = [lon,lat]
        if 'distance' in df.columns:
            a_row.append(np.nan)
        if 'waymark' in df.columns:
            a_row.append(np.nan)
        row = pd.Series(a_row,index=df.columns)
        df = df.append(row,ignore_index = True)
    
    return df

def calc_distances(df):
    
    distances = [0]
    lats = df['lat'].tolist()
    lons = df['lon'].tolist()
    
    for i in range(0,len(df)):

        if i > 0:
            prev_lon = lons[i-1]
            prev_lat = lats[i-1]
            
            delta_2D = haversine.haversine((prev_lat,prev_lon),(lats[i],lons[i])) * 1000
     
            new = distances[-1] + delta_2D
        
            distances.append(new)
            
    df['distance'] = distances
    
    return df

def load_df(next_file):
    try:
        df = pd.read_csv('custom_route.csv')
        file = next_file
    except:
        df = pd.DataFrame(columns=['lon','lat'])
        file = FIRST_FILE
        
    return df, file

for place in [NEXT_PLACE]:
    
    next_file = place + '.gpx'

    df, file = load_df(next_file)

    data = import_data(file)

    df = load_data(df, data)

    if 'waymark' in df.columns: #will only be present if using custom_route
        FIRST_PLACE = df.at[len(df)-1,'waymark']
    
        if place in df['waymark'].unique().tolist():
            raise ValueError (f'''You have already been to {place}.
Reconfigure the script to continue.''')
    else:
        df.at[0,'waymark'] = FIRST_PLACE

    df = calc_distances(df)

    df = df.reset_index(drop=True)

    df.at[len(df)-1,'waymark'] = place

    df.to_csv(r'custom_route.csv', index = False)

