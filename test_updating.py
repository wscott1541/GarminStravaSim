#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 15:25:52 2020

@author: WS
"""

import analyse

import pandas as pd

import os

from time import time
from datetime import datetime

file_name = "WSactivities.csv"
    
data = pd.read_csv(r'{}'.format(file_name))

df = pd.DataFrame(data,columns= ['Activity number','Activity Type','Date','Distance','Time'])

try:
    new_data = pd.read_csv(r'test_activities.csv')
    new = pd.DataFrame(new_data,columns= ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status'])
    prev = 1
    prev_activities = new['Activity number'].tolist()
except:
    new = pd.DataFrame(columns= ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status'])
    prev = 0

activities = df['Activity number'].tolist()
types = df['Activity Type'].tolist()
dates = df['Date'].tolist()
dists = df['Distance'].tolist()
times = df['Time'].tolist()

if prev == 1:
    last = len(prev_activities)
    ran = range(last-2,last+50)
else:
    ran = range(0,21)

for i in ran:
    if prev == 1:
        try:
            if prev_activities[i] == activities[i]:
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
                gpx_df = analyse.pull_gpx(row[0])
                today = time()
                today_dt = datetime.fromtimestamp(today)
                time_string = datetime.strftime(today_dt,'%H:%M:%S')
                print('Read activity {} GPX at {}'.format(i,time_string))
                status = 'Y'
            else:
                status = 'INVALID'
            
        if row[1] == 'Running':
            r_times = analyse.best_times_running(gpx_df)
        else:
            r_times = ['NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE','NONE']
            #[one_k, one_m, one_five, thr_m, fiv_k, ten_k, twe_k, half, full]
        if row[1] == 'Cycling':
            c_times = analyse.best_times_cycling(gpx_df)
        else:
            c_times = ['NONE','NONE','NONE','NONE','NONE','NONE']
                        #[ten_k, twe_k, fif_k, hun_k, t_h_k, t_f_k]
        new_row = [row[0],row[1],row[2],row[3],row[4],r_times[0],r_times[1],r_times[2],r_times[3],r_times[4],r_times[5],r_times[6],r_times[7],r_times[8],c_times[0],c_times[1],c_times[2],c_times[3],c_times[4],c_times[5],status]
    
        a_row = pd.Series(new_row,index=new.columns)
        mod_df = new.append(a_row,ignore_index = True)
        new = mod_df.sort_values(by='Date')
        new.to_csv(r'test_activities.csv',index=False)
    