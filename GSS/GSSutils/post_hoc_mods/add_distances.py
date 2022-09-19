#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 14:35:30 2022

@author: willscott
"""
import os
import numpy as np
import pandas as pd

from GSS.GSSutils import loading_modules as lm
from GSS.GSSutils import data_read as dr
#this means that this only works in the main folder!

df = dr.pull_data()

distance_str = '10 mile'
distances = dr.dist_dict
distance = distances[distance_str]/1000

if distance_str not in df.columns:
    df[distance_str] = 'NONE'

valid_activities = df[(df['Distance']>=distance)&(df['Activity Type']=='Running')]['Activity number'].tolist()#Running implied
known_activities = df[df[distance_str]!='NONE']['Activity number'].tolist()
known_invalidies = ['5042522225']

activities_to_check = [a for a in valid_activities if a not in known_activities+known_invalidies]
activities_to_check = activities_to_check#[:1]

#raise ValueError(known_activities,valid_activities)

def add_distance(a, distance_str):
    gpx_df = dr.route_data(a)
    
    gpx_df = lm.best_time_ws(distance_str, gpx_df, pull_time=False, known_time=False)
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    
    filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.csv'.format(a))
    
    if 'alt' not in gpx_df.columns:
        gpx_df['alt'] = np.nan
    
    deet_cols = ['lon','lat','alt','time','distance','HR']
    distance_cols = [c for c in distances if c in gpx_df.columns]
    
    gpx_df = gpx_df[deet_cols+distance_cols]
    
    gpx_df.to_csv(r'{}'.format(filename), index=False)
    
    time = lm.best_time_ws(distance_str,gpx_df,pull_time=True, known_time=True)
    
    df = dr.pull_data()
    
    if distance_str not in df.columns:
        df[distance_str] = 'NONE'
        
    deet_cols = ['Activity number','Activity Type', 'Date','Distance','Time','Shoes','Rise','Fall']
    distance_cols = [c for c in distances]
    other_cols = ['C10k','C20k','C50k','C100k','C200k','C250k','Notes','Admin']
    
    df = df[deet_cols+distance_cols+other_cols]
    
    df = df.set_index('Activity number')
    
    df.at[a,distance_str] = time
    
    df = df.reset_index(drop=False).rename(columns={'index': 'Activity number'})
    
    df.to_csv(r'{}'.format('activities.csv'),index=False) 
    
    print(f'{a}: {time}')

for a in activities_to_check:
    try:
        add_distance(a, distance_str)
    except:
        raise ValueError(a)