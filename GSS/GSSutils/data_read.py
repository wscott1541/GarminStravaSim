#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:18:49 2020

@author: WS
"""

import numpy as np
import pandas as pd

from . import today_string
y_day_string = today_string.y_day_string
from datetime import datetime, timedelta

import haversine
import gpxpy
from math import sqrt

import os
import json

from typing import Dict, Optional

import copy

cols = ['Activity number','Activity Type','Date','Distance','Time','Shoes','Rise','Fall','1km','1 mile','1.5 mile','3 mile','5km','5 mile','10km','10 mile','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Run Rankings','Notes','Admin']

dist_dict = {
    '1km': 1000,
    '1 mile': 1609.34,
    '1.5 mile': 2414.02,
    '3 mile': 4828.03,
    '5km': 5000,
    '5 mile': 8046.72,
    '10km': 10000,
    '10 mile': 16093.40,
    '20km': 20000,
    'Half': 21097.7,
    'Full': 42195
}

dist_list = list(dist_dict.keys())

if any(d for d in dist_list if d not in cols):
    raise ValueError('check all distances in cols')

'''
def pull_initials():
    user_data = pd.read_csv (r'users.csv')  
 
    users = pd.DataFrame(user_data, columns= ['Initials'])

    initials_list = users['Initials'].tolist()
    
    initials = initials_list[0]
    
    return(initials)
'''

def pull_data():
    return pd.read_csv (r'activities.csv')#.set_index('Activity number', drop=False) 
 
    #raise ValueError(data)
 
    #df = pd.DataFrame(data)

    #initials_list = users['Initials'].tolist()
    
    #initials = initials_list[0]
    
    #return(df)

def ac_detail(ac_number, detail): #weirdly, is there a reason not to load the lot of them as a dict?
    
    df = pull_data().set_index('Activity number', drop=False)
    
    deet = df.at[ac_number, detail]
    
    #df = df.reset_index()
    
    return deet

def ac_dict(ac_number: str)->Dict:#should really type this properly
    
    df = pull_data().set_index('Activity number', drop=False)
    
    return df.loc[ac_number].to_dict()

    #return {c: df.at[ac_number,c] for c in df.columns}
    
    #for c in df.columns:
    #    d[c] = df.at[ac_number, c]
    
    #return d

def pull_gpx_status(initials):
    user_data = pd.read_csv (r'users.csv')  
 
    users = pd.DataFrame(user_data, columns= ['GPX'])

    gpx_statii = users['GPX'].tolist()
    
    gpx_status = gpx_statii[0]
    
    return(gpx_status)    

def stringtime_to_floatminute(time_string):
        hours = float(time_string[:2])
        minutes = float(time_string[3:5])
        seconds = float(time_string[6:8])
    
        time = hours * 60 + minutes + seconds/60
    
        return(time)
'''
def pull_data():
    #file_name = "{}activities.csv".format(initials)
    
    #data = pd.read_csv(r'{}'.format(file_name))
    data = pd.read_csv(r'activities.csv')
    df = pd.DataFrame(data, columns= cols)
    #df = df.sort_values(by='Date')#sort_values is deprecated Python
    return(df)
'''
def data_read(initials):
    df = pull_data(initials)

    dates_times = df['Date'].tolist()
    dates = []
    for i in range(0,len(dates_times)):
        useful_dates = dates_times[i][0:10]
        dates.append(useful_dates)#in format string 'yyyy-mm-dd'
    #I don't know if this is even necessary, but I don't want to try to amend every this to working in datetime

    """    
    from datetime import datetime
    new_dates = []
    for i in range(0,len(dates)):
        datetime_strp = datetime.strptime(dates_times[i],'%Y-%m-%d %H:%M:%S')
        datetime_object = datetime.timestamp(datetime_strp)
        new_dates.append(datetime_object)

    """

    #make distances useable
    distances = df['Distance'].tolist()

    #make durations useable
    #duration_times = df['Time'].tolist()
    duration_strings = df['Time'].tolist()
    
    durations = []
    for i in range(0,len(duration_strings)):
        dur = stringtime_to_floatminute(duration_strings[i])
        durations.append(dur)
    
    types = df['Activity Type'].tolist()
    
    return(dates,distances,durations,types)
    
def all_times(initials,distance):
    df = pull_data(initials)
    
    types = df['Activity Type'].tolist()
    dates = df['Date'].tolist()
    dists = df['Distance'].tolist()
    splits = df[distance].tolist()
    
    return(types,dates,dists,splits)
    
def week_times(initials,distance):
    all_types,all_dates,all_dists,all_splits = all_times(initials,distance)
    
    y_day_obj = datetime.strptime(y_day_string,'%Y-%m-%d')
    
    last_week = y_day_obj - timedelta(days=7)
    
    types = []
    dates = []
    dists = []
    splits = []
    
    for i in range(0,len(all_dates)):
        stamp = all_dates[i][:10]
        obj = datetime.strptime(stamp,'%Y-%m-%d')
        
        if obj > last_week:
            types.append(all_types[i])
            dates.append(all_dates[i])
            dists.append(all_dists[i])
            splits.append(all_splits[i])
            
    return(types,dates,dists,splits)

def activity_details(user_df,activity_number,field):  

    if field == 'Duration':
        field = 'Time'
    elif field == 'Type':
        field = 'Activity Type'
    
    # index = user_df[user_df['Activity number'] == activity_number].index.values[0]
    
    # value = user_df.at[index,field]
    
    user_df = user_df.set_index('Activity number', drop=False)
    
    return user_df.at[activity_number, field] 
    
    
    '''
    ac_numbers = user_df['Activity number'].tolist()
    types_list = user_df['Activity Type'].tolist()
    dates = user_df['Date'].tolist()
    distances = user_df['Distance'].tolist()
    durs = user_df['Time'].tolist()
    shoes = user_df['Shoes'].tolist()
    
    ac_type = []
    date = []
    dist = []
    dur = []
    shoe = []
    
    for i in range(0,len(ac_numbers)):
        if activity_number == ac_numbers[i]:
            ac_type.append(types_list[i])
            date.append(dates[i])
            dist.append(distances[i])
            dur.append(durs[i])
            shoe.append(shoes[i])
    
    if 'Type' in field:
        value = ac_type[0]
    if 'Date' in field:
        value = date[0]
    if 'Distance' in field:
        value = dist[0]
    if 'Duration' in field or 'Time' in field:
        value = dur[0]
    if 'Shoes' in field:
        value = shoe[0]
    '''
    
    # return(value)

def activity_splits(user_df,activity_number,distance):
    
    #user_df = user_df.loc[user_df['Activity number'] == activity_number]
    
        #ac_numbers = user_df['Activity number'].tolist()
    #splits = user_df[distance].tolist()
    
        #split_list = []
        #for i in range(0,len(ac_numbers)):
            #    split_list.append(splits[i])
    
    #split = splits[0]
    #print(activity_number,distance)
    
    #index = user_df.loc[user_df['Activity number'] == activity_number].index.values[0]
    #print(index)
    #split = user_df.at[index,distance]
    #print(split)
    
    return activity_details(user_df, activity_number, distance)

#user_df = pull_data('WS')
#print(activity_details(user_df,'AB4H2007','Shoes'))
    
def split_rank(user_df,activity_number,distance,kind='all'):
    #df = df.sort_values(by=distance)
    
    #df.to_csv(r'check-sorting.csv')
    
    ac_type = activity_details(user_df,activity_number,'Type')
    
    user_df = user_df.loc[user_df['Activity Type'] == ac_type]
    
    ac_numbers = user_df['Activity number'].tolist()
    #ac_types = user_df['Activity Type'].tolist()
    splits = user_df[distance].tolist()
    
    
    split = activity_splits(user_df,activity_number,distance)
    
    n = 1
    stop = 0
    if split != 'NONE':
        while stop == 0:
            if kind == 'all':
                for i in range(0,len(splits)):
                    if splits[i] < split:
                        n += 1
                    if i == (len(splits) - 1):
                        stop = 1
            else:
                for i in range(0,len(splits)):
                    if splits[i] < split and stop == 0:
                        n += 1
                    
                    if activity_number == ac_numbers[i]:
                        stop = 1
    
    if split == 'NONE':
        n = 'NONE'
    
    return(n)
            
def split_count(user_df,split,ac_no='none',kind='all'):
    
    if ac_no != 'none':
        ac_date = ac_detail(ac_no,'Date')
        user_df = user_df.loc[user_df['Date'] <= ac_date]
    
    #ac_numbers = user_df['Activity number'].tolist()
    splits = user_df[split].tolist()
    #dates = user_df['Date'].tolist()
    
    #ac_type = activity_details(user_df,activity_number,'Type')
    
    n = 0
    for i in range(0,len(splits)):
        if splits[i] != 'NONE':
            n += 1           
                
    return(n)

def split_extremes(user_df,distance,extreme):
    
    splits = user_df[distance].tolist()
    
    filter_splits = []
    
    for i in range(0,len(splits)):
        if 'NONE' not in splits[i]:
            filter_splits.append(splits[i])
    
    if 'ax' in extreme:
        output = max(filter_splits)
    
    if 'in' in extreme:
        output = min(filter_splits)
        
    return(output)

def split_percentile(user_df,distance,percentile):
    
    splits = user_df[distance].tolist()
    
    filter_splits = []
    
    for i in range(0,len(splits)):
        if 'NONE' not in splits[i]:
            filter_splits.append(splits[i])
            
    filter_splits.sort()
    
    if percentile > 1:
        percentile = percentile /100
    
    val = round(percentile * len(filter_splits))
    
    if val == len(filter_splits):
        val = val - 1
    
    output = filter_splits[val]
    
    return(output)
    
#ws_df = pull_data('WS')
#split_percentile(ws_df,'1km',95)
    
    
def latest_activity():
    df = pull_data()
    
    ac_numbers = df['Activity number'].tolist()

    latest = ac_numbers[-1]
    
    return(latest)

""""ROUTE DATA PULL"""

def simple_gpx_pull(filename):
    
    #fileDir = os.path.dirname(os.path.realpath('__file__'))

    #filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.gpx'.format(activity_number))
    
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
'''    
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
    if len(activity_number) == 8 or len(activity_number) == 9:
        df = pull_csv(activity_number)
        
    return(df)
'''

def generate_gpx_archive_filename(activity_number: str)->str:
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    
    return os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.csv'.format(activity_number))

def pull_csv_pd(activity_number, option='column_name'):

    filename = generate_gpx_archive_filename(activity_number)
    
    #I think I only need distance and time
    
    #if option == 'column_name':
    #    data = pd.read_csv(r'{}'.format(filename))
    #    df = pd.DataFrame(data,columns=['lon','lat','time','distance','HR'])
    #else:
    #    data = pd.read_csv(r'{}'.format(filename))
    #    df = pd.DataFrame(data,columns=['lon','lat','time','distance','HR',option])
    
    data = pd.read_csv(r'{}'.format(filename))
    df = pd.DataFrame(data)#because just get all the columns?
    
    df['time'] = df['time'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    
    return(df)

def route_data(activity_number, option='column_name'):

    df = pull_csv_pd(activity_number, option)
        
    return(df)    
    
class Activity:
    
    def strftime(self, fmt):
        return datetime.strftime(self.date_dt, fmt)
    
    def fmt_alt(self, alt: str)->float:
        if alt == 'NONE':
            return np.nan
        else:
            return float(alt)
    
    def fmt_alt_change(self, alt_change):
        if alt_change:
            return f'{abs(alt_change)}m'
        else:
            return ''
    #think about which of these should be callable elsewhere (include in the class) and which should not (separate)
    
    
    def __init__(self, activity_id):
        self.activity_id = activity_id
        self.activity_dict = ac_dict(activity_id)
        self._route_data = None
        
        #Date-related qualities
        self.date_str = self.activity_dict['Date']
        self.date_dt = datetime.strptime(self.date_str, '%Y-%m-%d %H:%M:%S')# if isinstance(self.date_str, str) else self.date_str
        self.date = self.strftime('%Y-%m-%d')
        self.time = self.strftime('%H:%M:%S')
        self.year, self.month, self.day = (round(float(self.strftime(fmt))) for fmt in ('%Y', '%m', '%d'))
        #round(float(self.strftime('%Y'))), round(float(self.strftime('%m'))), round(float(self.strftime('%d')))

        #altitude-related qualities
        self.ascent = self.fmt_alt(self.activity_dict['Rise'])
        self.descent = self.fmt_alt(self.activity_dict['Fall'])
        self.ascent_str = self.fmt_alt_change(self.ascent)
        self.descent_str = self.fmt_alt_change(self.descent)
       
    @property
    def route_data(self)->pd.DataFrame:
        if self._route_data:
            pass
        else:
            self._route_data = pull_csv_pd(self.activity_id)
        
        return self._route_data
    
    
        
class Activities:
    
    def strftime_col(self, column, fmt)->pd.Series:
        return self.df[column].apply(lambda x: datetime.strftime(x, fmt))
        
    def __init__(self, filters: Optional[Dict]={}):
        self.df = pd.read_csv (r'activities.csv')
        self.df['Date'] = self.df['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        self.df['Time'] = pd.to_timedelta(self.df['Time'])
        self.df['Run Rankings'] = self.df['Run Rankings'].apply(lambda x: json.loads(x.replace("'",'"')))
        
        self.personal_bests = {k:{} for k in dist_list}
        
        self._unique_activities = None
        self._active_days = None
        self._sum_distance = None
        self._mean_distance = None
        self._sum_time = None
        
    def col_filter(self, filters: Dict)->None:
        for k, v in filters.items():
            self.df = self.df[self.df[k]==v]
        return self
    
    def date_filter(self, str_fmt: str, value: str):
        
        dates = self.strftime_col('Date', str_fmt)
        
        self.df = self.df[dates==value]
        
        return self
    
    def deep_copy(self):
        return copy.deepcopy(self)
    
    def quickest_time(self, column)->str:#unconverted timedelta str, but str nonethless
        if self.personal_bests[column].get('quickest_time'):
            pass
        else:
            self.personal_bests[column]['quickest_time'] = self.df[self.df[column]!='NONE'][column].min()
            
        return self.personal_bests[column]['quickest_time']
    
    def pb_activity(self, column)->str:
        
        if self.personal_bests[column].get('ac_id'):
            pass
        else:
            pb = self.quickest_time(column)
            df = self.df[self.df[column]==pb]
            
            if df.empty:
                ac_id = None
            else:
                ac_id = df['Activity number'].tolist()[0]
                
            self.personal_bests[column]['ac_id'] = ac_id        
        
        return self.personal_bests[column]['ac_id']
    
    def n_pbs(self, column)->float:
        if self.personal_bests[column].get('n_pbs'):
            pass
        else:
            n = 0
            for r in self.df['Run Rankings']:
                if column in r.get('1st', []):
                    n += 1
            self.personal_bests[column]['n_pbs'] = int(n)
        
        return self.personal_bests[column]['n_pbs']

    @property
    def unique_activities(self)->float:
        if self._unique_activities:
            pass
        else:
            self._unique_activities = len(self.df)
        
        return self._unique_activities
    
    @property
    def active_days(self)->float:
        if self._active_days:
            pass
        else:            
            self._active_days = self.strftime_col('Date', '%Y-%m-%d').nunique()
        
        return self._active_days
    @property
    def sum_distance(self)->float:
        if self._sum_distance:
            pass
        else:
            self._sum_distance = self.df['Distance'].sum()
       
        return self._sum_distance
    @property
    def mean_distance(self)->float:
        if self._mean_distance:
            pass
        else:
            self._mean_distance = self.df['Distance'].mean()
        
        return self._mean_distance
    @property
    def sum_time(self)->timedelta:
        if self._sum_time:
            pass
        else:                        
            self._sum_time = self.df['Time'].sum()
            
        return self._sum_time