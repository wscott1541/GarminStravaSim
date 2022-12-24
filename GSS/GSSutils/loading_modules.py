# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:18:10 2020

@author: WS
"""

import os

import pandas as pd

from fitparse import FitFile

from GSS.GSSutils import today_string as ts

from datetime import datetime, timedelta
import time

import gpxpy

import haversine
from math import sqrt

from typing import Dict, List

#import data_read as dr

from GSS.GSSutils import data_read as dr

#import analyse

from numpy import NaN, nan,isnan

import urllib.request, json

def action_log(action_dictionary):

    filename = 'usage_log.csv'
    
    try:
        data = pd.read_csv(filename)
        log = pd.DataFrame(data,columns=['timestamp','page_type','detail','mode'])
    except:
        log = pd.DataFrame(columns=['timestamp','page_type','detail','mode'])
        
    action_df = pd.DataFrame.from_dict(action_dictionary)
    log = log.append(action_df)
    log.to_csv(filename)
    
def get_timestamp():
    today = time.time()

    today_dt = datetime.fromtimestamp(today)
    
    timestamp = datetime.strftime(today_dt,'%Y-%m-%d %H:%M:%S')

    return(timestamp)
    
conversion = 180 / (2 ** 31)

def create_nans(x):
    if str(x)[-8:] == '00:00:00':
        x = NaN
    return(x)

def convert_time(x):
    if str(type(x))  == "<class 'str'>":
        x = datetime.strptime(x,'%Y-%m-%d %H:%M:%S')
    return(x)

def sort_by_date(filename:str='activities.csv')->None:
    df = pd.read_csv(r'{}'.format(filename))
    df = df.sort_values(by='Date', ascending=True)
    df.to_csv(r'{}'.format(filename))    

def best_time_ws(distance,gpx_df,pull_time=False, known_time=False):
    
    distance_numeral = dr.dist_dict[distance]
    
    #print('start')
    #time_check()
    distances = gpx_df['distance'].tolist()
    #times = gpx_df['time'].tolist()
    
    indexes = []
    
    if known_time and distance in gpx_df.columns:
        #implies that this has already been logged and, therefore, we don't actually need to recalculate
        times = gpx_df[gpx_df[distance]==1]['time'].tolist()
        start = datetime.strptime(times[0], '%Y-%m-%d %H:%M:%S') if isinstance(times[0], str) else times[0]
        finis = datetime.strptime(times[-1], '%Y-%m-%d %H:%M:%S') if isinstance(times[-1], str) else times[-1]
        best_time_known = finis - start
    elif known_time and distance not in gpx_df.columns:
        best_time_known = 'NONE'
        
    
    if distances[-1] > distance_numeral and not known_time:
    
        for i in range(0,len(gpx_df)):
        
            i_s = []
            v = 1
        
            while len(i_s) < 1 and distances[i] > distance_numeral and i >= v:
                #print(i,v)
                if (distances[i] - distances[i-v]) > distance_numeral and (distances[i] - distances[i-v] < distance_numeral + 100):
                    i_s.append(i-v)
                v += 1
        
        # for v in range(0,i):
            #
                #if len(i_s) < 1 and (distances[i] - distances[i-v]) > distance_numeral and (distances[i] - distances[i-v] < distance_numeral + 100):
                    #   i_s.append(i-v)
                
            if len(i_s) > 0:
                indexes.append(i_s[0])
            else:
                indexes.append(NaN)#was NaN
    
    #gpx_df = gpx_df.index[gpx_df['distance'] < (distance - 1000)].tolist()[-1:]
    
   # print('first loop')
    #time_check()
    
        gpx_df[f'{distance} indexes'] = indexes
    
    #print(gpx_df)
    
    #print(type(gpx_df['time'][0]))
        if str(type(gpx_df['time'][0])) == 'str':#only if full loop
            gpx_df['time'] = gpx_df['time'].apply(lambda x : datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    #print(type(gpx_df['time'][0]))
        gpx_df[f'{distance} indexes'] = gpx_df[f'{distance} indexes'].apply(lambda x: int(x) if not isnan(x) else NaN) 
    
    #print(gpx_df[f'{distance} indexes'])
    #gpx_df = gpx_df.reset_index()
    #gpx_df['ref time'] = gpx_df['time'][gpx_df[f'{distance} indexes']]
    
        #ref_times = []
        #for i in range(0,len(gpx_df)):
        #    ref_time = gpx_df['time'][gpx_df[f'{distance} indexes'][i]]
        #    ref_times.append(ref_time)
        #gpx_df['ref_times'] = ref_times
        
    #print(len(ref_times))
        gpx_df['ref_times'] = gpx_df[f'{distance} indexes'].apply(lambda x: gpx_df.at[x,'time'] if not isnan(x) else NaN)
    
        gpx_df[f'{distance} time'] = gpx_df['time'] - gpx_df['ref_times']
        gpx_df[f'{distance} time'] = gpx_df[f'{distance} time'].apply(create_nans)
        best_time = (gpx_df[f'{distance} time'].min())
        idx_end = gpx_df[f'{distance} time'].idxmin()
        idx_sta = gpx_df[f'{distance} indexes'][idx_end]
    #print(gpx_df[f'{distance} indexes'][idx_min])
    #print(gpx_df['time'][idx_min])
    #print(gpx_df['time'][1238])
    
        best = []
        for i in range(len(gpx_df)):
            if i < idx_sta:
                best.append(0)
            elif i > idx_end:
                best.append(2)
            else:
                best.append(1)
    
        gpx_df[f'{distance}'] = best
    
        gpx_df = gpx_df.drop(['ref_times',f'{distance} time',f'{distance} indexes'],axis=1)
    #gpx_df[['lon','lat','time','distance','alt','HR',f'{distance}']]#better with drop
    
    #print(gpx_df)
    
        print(distance, 'complete')
        print(best_time)
    elif known_time and pull_time:
        print(distance, 'pre-found')
        print(best_time_known)
    else:
        best_time = 'NONE'
        print(distance,'not found')
    
    if pull_time and known_time:
        return best_time_known
    elif pull_time == True:
        return(best_time)
    else:     
        return(gpx_df)
    
#from bs4 import BeautifulSoup

#from geopy.geocoders import Nominatim

def pull_alt_json(pulls_string,alt_df,rtrn = False):
    
    lats = []
    lons = []
    alts = []
    
    europe_top_map = 'eudem25m'
    usa_top_map = 'ned10m'
    
    top_map = europe_top_map
    
    link = f'https://api.opentopodata.org/v1/{top_map}?locations={pulls_string}'
    #https://www.opentopodata.org/

    try:
        with urllib.request.urlopen(link) as url:
            data = json.loads(url.read().decode())
    except:
        print(link)
        with urllib.request.urlopen(link) as url:
            data = json.loads(url.read().decode())
        
    results = data['results']
    
    for i in range(0,len(results)):
        result = results[i]
        alts.append(result['elevation'])
        lats.append(result['location']['lat'])
        lons.append(result['location']['lng'])
    
    df = pd.DataFrame({'lat': lats,
          'lon': lons,
          'alt': alts})
    
    alt_df = alt_df.append(df)
    
    alt_df['lat'] = alt_df['lat'].apply(lambda x: round(x,5))
    alt_df['lon'] = alt_df['lon'].apply(lambda x: round(x,5))
    alt_df['alt'] = alt_df['alt'].apply(lambda x: round(x,1))
    
    alt_df = alt_df.drop_duplicates(subset=['lat', 'lon'], keep='first')
    
    alt_df = alt_df.sort_values(by=['lat','lon'])
    
    alt_df.to_csv('altitudes.csv', index=False)
    
    if rtrn == True:
        return(alt_df)

def pull_alts(ac_df,alt_df,rtrn=False):
    
    lats = ac_df['lat'].tolist()
    lons = ac_df['lon'].tolist() 
    
    pulls = ''
    reqs = 0
    
    for i in range(0,len(lats)):
        spot = alt_df.loc[alt_df['lat'] == round(lats[i],5)]
        spot = spot.loc[spot['lon'] == round(lons[i],5)]
        
        if i % 25 == 0:
            print('pull',i,'/',len(lats))
            print('req',reqs)
        
        if len(spot) == 0:
            
            if len(pulls) == 0:
                
                pulls = pulls + f'{round(lats[i],5)}' + ',' + f'{round(lons[i],5)}' 
            
            else:
                
                pulls = pulls + '|' + f'{round(lats[i],5)}' + ',' + f'{round(lons[i],5)}' 
                
            reqs += 1
            
        if reqs == 95:
            
            alt_df = pull_alt_json(pulls,alt_df,rtrn = True)
            
            pulls = ''
            reqs = 0
            
    if reqs > 0:
        
        alt_df = pull_alt_json(pulls,alt_df, rtrn = True)
        
    if rtrn == True:
        return (alt_df)
        
def update_alt_db(ac_df,alt_df):
    
    n_df = ac_df[['lat','lon','alt']]
        
    alt_df = alt_df.append(n_df)
    
    alt_df['lat'] = alt_df['lat'].apply(lambda x: round(x,5))
    alt_df['lon'] = alt_df['lon'].apply(lambda x: round(x,5))
    alt_df['alt'] = alt_df['alt'].apply(lambda x: round(x,1))

    alt_df = alt_df.drop_duplicates(subset=['lat', 'lon'], keep='first')

    alt_df = alt_df.sort_values(by=['lat','lon'])
    
    alt_df.to_csv('altitudes.csv', index=False)
        
def save_alt_col(ac_df,alt_df,file_location):

    lats = ac_df['lat'].tolist()
    lons = ac_df['lon'].tolist()
    alts = []
    
    for i in range(0,len(lats)):
        
        if i % 25 == 0:
            print('save',i,'/',len(lats))
        
        spot = alt_df.loc[alt_df['lat'] == round(lats[i],5)]
        spot = spot.loc[spot['lon'] == round(lons[i],5)]
        
        alt = spot['alt'].tolist()[0]
        alts.append(alt)
        
    ac_df['alt'] = alts
        
    #f_name = f'activity_{activity_number}.csv'
    
    print(ac_df.columns)
    
    #input('cont?')

    ac_df.to_csv(file_location, index=False)
    
def rising(x):
    
    if x < 0:
        x = 0
        
    return(x)

def falling(x):
    
    if x > 0:
        x = 0
        
    return(x)

def ascent_descent(ac_df):
    try:
        
        #ac_data = pd.read_csv(f'activity_{ac_numbs[i]}.csv')

        alt_df = ac_df[['alt']]
    
        #alt_df['check'] = alt_df['alt'].apply(round_func)
        
        alt_df['alt'] = alt_df['alt'].rolling(60,min_periods=1).mean()
        alt_df['alt'] = alt_df['alt'].apply(lambda x: round(x,1))
    
    
        alt_df['diff'] = alt_df['alt'].diff()
    
        #print(alt_df['diff'].head())
    
        alt_df['rises'] = alt_df['diff'].apply(lambda x : rising(x))
    
        #print('here?')
    
        alt_df['falls'] = alt_df['diff'].apply(falling)
            
        rise = round(alt_df['rises'].sum(),1)
        fall = round(alt_df['falls'].sum(),1)
        
        #print(rise)
    
        if rise == 0.0 and fall == 0.0:
            rise = 'NONE'
            fall = 'NONE'
            #print('rbk')

    except:
        rise = 'NONE'
        fall = 'NONE'
        
    return (rise, fall)

def add_run_rankings(df: pd.DataFrame, times: Dict[str, timedelta], date: datetime.date, a_type:str) -> Dict[str, List[str]]:
    
    rankings = {
        '1st': [],
        '2nd': [],
        '3rd': []
        }
    
    for dist in dr.dist_dict:
        t = times.get(dist, 'NONE')

        if a_type == 'Running':
            d_df = df[(df['Date']<str(date))&(df[dist]<=str(t))&(df[dist]!='NONE')]
        
        #if '2022-09-17' in str(date) and dist == '1.5 mile':
        #    print(d_df, d_df[dist].unique())
        
        if a_type != 'Running':
            rankings = {}
        elif t == 'NONE':
            pass
        elif len(d_df[dist].unique()) == 0:
            rankings['1st'].append(dist)
        elif len(d_df[dist].unique()) == 1:
            rankings['2nd'].append(dist)
        elif len(d_df[dist].unique()) == 2:
            rankings['3rd'].append(dist)
    
    return rankings

def assess_main(main_df,gpx_df,ac_details,main_df_name='activities.csv'):
    df = main_df

    #ac_abbr,activity,date, dist,full_string,shoes

    print('Loading activity {}'.format(len(df)))
    row = []
    times_dict = {}
    if ac_details['type'] == 'Running':
        
        for i in range(0,len(dr.dist_list)):
            best_time = best_time_ws(dr.dist_list[i], gpx_df, pull_time=True, known_time=True)
            row.append(best_time)
            times_dict[dr.dist_list[i]] = best_time
        for i in range(0,6):##This is, in effective, padding
            row.append('NONE')
        #status = 'CSV'
    else:
        measured_distances = len(dr.dist_dict) + 6#six cycling distances
        for i in range(0,measured_distances):#this needs to be the lengdf
            row.append('NONE')
        
        #status = 'NONE'

    series = [ac_details['no'],ac_details['type'],ac_details['date'],ac_details['dist'],ac_details['time'],ac_details['shoes']] 
    
    #ADD RISES AND FALLS
    ascent, descent = ascent_descent(gpx_df)
    series.append(ascent)
    series.append(descent)
    
    for i in range(0,len(row)):
        series.append(row[i])
    
    rankings = add_run_rankings(main_df, times_dict, ac_details['date'], ac_details['type'])
    series.append(rankings)
        
    series.append(ac_details['notes'])
    series.append('')#admin notes - going to have to be modified by hand
    
    
    try:
        a_row = pd.Series(series,index=main_df.columns)#this should be done with a replace if the activity exists, else append
    except:
        raise ValueError(main_df.columns,len(main_df.columns), series, len(series), len(dr.dist_dict) + 6)#six cycling distances)
    main_df = main_df.append(a_row,ignore_index = True)
    
    #main_df = main_df.sort_values(by='Date', ascending = True)
    #doesn't work because some are timestamps and some are strings
    
    main_df.to_csv(r'{}'.format(main_df_name),index=False) 


def activity_import(FIT='NONE',gpx='NONE',activity='auto',shoes='default',email_option=True,alt_option=True,notes=''):

    #set-up
    #initials = dr.pull_initials()
    
    if ('FIT' not in FIT) and (FIT != 'NONE'):
        FIT = FIT + '.FIT'
    
    if ('gpx' not in gpx) and (gpx != 'NONE'):
        gpx = gpx + '.gpx'
        
    if gpx != 'NONE':
        
        name_options = 'ABCDE'
        
        available_options = []
        
        latest_name = dr.latest_activity()
        
        for i in range(0,len(name_options)):
            if  f'{name_options[i]}{ts.year}{ts.month}{ts.day}' != latest_name:
                available_options.append(f'{name_options[i]}{ts.year}{ts.month}{ts.day}')
        
        ac_abbr = available_options[0]
    else:
        pos = FIT.find('.FIT')
        
        ac_abbr = FIT[:pos] 
        
    print(f'Importing {ac_abbr}')
        
    #read files
    
    timestamps = []
    distances = []

    if FIT != 'NONE' and gpx == 'NONE':
        
        print('Loading FIT')
        
        fitfile = FitFile(FIT)
        
        heart_rates = []
        latitudes = []
        longitudes = []
        cadences = []
        
    # Get all data messages that are of type record
        for record in fitfile.get_messages('record'):

            for record_data in record:
                
                if record_data.name == 'timestamp':
                    timestamps.append(record_data.value)
                if record_data.name == 'position_lat':
                    latitudes.append(record_data.value)
                if record_data.name == 'position_long':
                    longitudes.append(record_data.value)
                if record_data.name == 'heart_rate':
                    heart_rates.append(record_data.value)
                if record_data.name == 'distance':
                    distances.append(record_data.value)
                if record_data.name == 'cadence':
                    cadences.append(record_data.value)
        
        df = pd.DataFrame(columns=['time','lat','lon','HR','distance','cadence'])

        lat_breaks = []
        #lat_break_checks = []
        lon_breaks = []
        #lon_break_checks = []

        for i in range(0,len(timestamps)):
    
            if activity != 'Cardio':
                try:
                    #print(i,latitudes[i])
                    lat = latitudes[i] * conversion
                    if len(lat_breaks) > 0:
                        lat_breaks = []
                except:
                    if len(lat_breaks) == 0:
                        lat_breaks.append(latitudes[i-1] * conversion)
                    #elif lat_break_checks[-1] == i - 1:
                    #    here = 'junk'
                    #else:
                    #    lat_breaks.append(lat_break)
                        
                    lat = lat_breaks[-1]

                try:
                    lon = longitudes[i] * conversion
                    if len(lon_breaks) > 0:
                        lon_breaks = []
                except:
                    if len(lon_breaks) == 0:
                        lon_breaks.append(longitudes[i-1] * conversion)
                    #elif lon_break_checks[-1] == i - 1:
                    #    here = 'junk'
                    #else:
                    #    lon_breaks = [longitudes[i-1] * conversion]
                    #    lon_break_checks.append(i)    
        
                    lon = lon_breaks[-1]
                
            else:
                lat = 'NONE'
                lon = 'NONE'
    
            timestamp = timestamps[i] + timedelta(hours=1)
        
            row = [timestamp,lat,lon,heart_rates[i],distances[i],cadences[i]]
            a_row = pd.Series(row,index=df.columns)
            df = df.append(a_row,ignore_index=True)

    if FIT != 'NONE' and gpx != 'NONE':
        
        print('Loading FIT')
        
        fitfile = FitFile(FIT)
        
        fit_ts = []
        fit_hr = []

        for record in fitfile.get_messages('record'):

            # Go through all the data entries in this record
            for record_data in record:
        
        #print(record_data)
        
                if record_data.name == 'timestamp':
                    fit_ts.append(record_data.value)
                if record_data.name == 'heart_rate':
                    fit_hr.append(record_data.value)
        
        print('Loading gpx')
        
        try:
            gpx_file = open(gpx)
            gpx_unpacked = gpxpy.parse(gpx_file)

            data = gpx_unpacked.tracks[0].segments[0].points
            
            print(data[0])
            
            stop = 0
        except:
            stop = 1
            gjgjg = ggjjg
            print('Early break')

        df = pd.DataFrame(columns=['lon','lat','alt','time','distance','HR'])
        #df = pd.DataFrame(columns=['lon','lat','alt'])

        #distances.append(0)

        hrs = []
        fit_s = convert_time(fit_ts[0])
        fit_f = convert_time(fit_ts[-1])
        
        print('Matching FIT to gpx')

        if stop == 0:
            for i in range(0,len(data)):
                #print(i)
                lon = data[i].longitude
                lat = data[i].latitude
                alt = data[i].elevation
        
                time_str = str(data[i].time)[:19]
                time_dt = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
                
                if time_dt >= fit_s and time_dt <= fit_f:
                    timestamps.append(time_dt)
        
                hr_found = False
        
                #while hr_found == False:
            
                for n in range(0,len(fit_ts)):
                    if time_dt == fit_ts[n] and hr_found == False:
                        hrs.append(fit_hr[n])
                        #print(f'{i}/{len(fit_ts)}',fit_hr[n])
                        hr_found = True
               
                try:
                    hr = hrs[-1]
                except:
                    hr = NaN

                if len(distances) > 0:
                    prev_lon = data[i-1].longitude
                    prev_lat = data[i-1].latitude
                    prev_alt = data[i-1].elevation
                
                    delta_2D = haversine.haversine((prev_lat,prev_lon),(lat,lon)) * 1000
                    
                    delta_alt = alt - prev_alt
                    
                    distance_3D = sqrt((delta_2D ** 2) + (delta_alt ** 2))
                
                    new = distances[-1] + distance_3D
                    
                    if time_dt >= fit_s and time_dt <= fit_f:
                        distances.append(new)
                else:
                    if time_dt >= fit_s and time_dt <= fit_f:
                        distances.append(0)
                    
                if time_dt >= fit_s and time_dt <= fit_f:
                    distance = distances[-1]

                if time_dt >= fit_s and time_dt <= fit_f:
                    a_row = [lon,lat,alt,time_dt,distance,hr]
                    row = pd.Series(a_row,index=df.columns)
                    df = df.append(row,ignore_index = True)
                
        #df['time'] = df['time'].apply(convert_time)
        
        #df = df.loc[df['time'] >= fit_s]
        #df = df.loc[df['time'] <= fit_f]
    
    if FIT == 'NONE' and gpx != 'NONE':
        
        print('Loading gpx')
        
        try:
            gpx_file = open(gpx)
            gpx_unpacked = gpxpy.parse(gpx_file)

            data = gpx_unpacked.tracks[0].segments[0].points
        
            stop = 0
        except:
            stop = 1
            print('Early break')

        df = pd.DataFrame(columns=['lon','lat','alt','time','distance','HR'])

        distances.append(0)

        if stop == 0:
            for i in range(0,len(data)):
                lon = data[i].longitude
                lat = data[i].latitude
                alt = data[i].elevation
                try:
                    ext = data[i].extensions[0].getchildren()[0]
                    hr = int(ext.text)
                except:
                    hr = 'NONE'
        
                time_str = str(data[i].time)[:19]
                time_dt = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
                timestamps.append(time_dt)

                if i > 0:
                    prev_lon = data[i-1].longitude
                    prev_lat = data[i-1].latitude
                    prev_alt = data[i-1].elevation
                
                    delta_2D = haversine.haversine((prev_lat,prev_lon),(lat,lon)) * 1000
                    
                    delta_alt = alt - prev_alt
                    
                    distance_3D = sqrt((delta_2D ** 2) + (delta_alt ** 2))
                
                    new = distances[-1] + distance_3D
        
                    distances.append(new)
                
                distance = distances[-1]

                a_row = [lon,lat,alt,time_dt,distance,hr]
                row = pd.Series(a_row,index=df.columns)
                df = df.append(row,ignore_index = True)

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    
    #rename ac_abbr here
    filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.csv'.format(ac_abbr))
    
    df.to_csv(r'{}'.format(filename), index = False)
    
    print(df)
    print(filename)
    
    #end of activity imports
    print('alt_option', alt_option)
    if alt_option == True and activity != 'Cardio':
        
        print('Loading altitudes')
            
        alt_data = pd.read_csv('altitudes.csv')
        altitudes_df = pd.DataFrame(alt_data)
        
        print(f'{len(altitudes_df)} altitudes loaded')
        
        if 'alt' not in df.columns:
            
            print('Finding altitudes')
            
            altitudes_df = pull_alts(df,altitudes_df,rtrn=True)#goes through the activity, fetches any lat/lons that do not have an alt
            
            print('Altitudes found')
            
            save_alt_col(df,altitudes_df,filename)#creates the alt column in df & saves
        
        else:
            try:
                alt_check = df['alt'].apply(lambda x: int(x))#breaks if empty nans; doesn't if not
                
                print('Updating altitudes db')
                
                update_alt_db(df,altitudes_df)
                #if doesn't break, add to altitides db
                
            except:#but if breaks...            
                print('Matching coordinates')
            
                altitudes_df = pull_alts(df,altitudes_df,rtrn = True)#goes through the activity, fetches any lat/lons that do not have an alt
            
                save_alt_col(df,altitudes_df,filename)#creates the alt column in df & saves
        
        print('Altitudes saved') 
    
    #break if just importing GPX here

    #file_name = "activities.csv".format(initials)
    
    data = pd.read_csv(r'activities.csv')
    
    #gpx_status = dr.pull_gpx_status(initials)
    
    #if gpx_status == 'Y':
    #    archive = pd.DataFrame(data, columns= dr.cols)
    #else:
    #    archive = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time'])    

    #initial archiving
    archive = pd.DataFrame(data)
    archname = os.path.join(fileDir, 'Archive.gitignore/{}activities.csv'.format(ts.today_string))
    archive.to_csv(r'{}'.format(archname), index = False)

    date = timestamps[0] + timedelta(hours=1)
    dist = round((distances[-1]/1000),2)
    full_td = timestamps[-1] - timestamps[0]
    full_secs = full_td.total_seconds()
    full_string = time.strftime('%H:%M:%S',time.gmtime(full_secs))

    pace = full_secs/dist

    if activity == 'auto':
        if pace < 240 and dist >= 15:
            activity = 'Cycling'
            #shoes = 'NONE'
        elif pace >= 181 and pace <= 570:
            activity = 'Running'
            #shoes = 'Kalenji Run Support Red'
            #shoes = 'Hoka One One Clifton 6'
        elif pace > 570:
            activity = 'Walking'
            #shoes = 'Merrell Vego 2019'
            
    if activity == 'Cardio':
        shoes = 'NONE'
        
    if shoes == 'default':
        if activity == 'Cycling':
            shoes = 'NONE'
        if activity == 'Running':
            shoes = 'Altra Torin 5'
            #'Hoka One One Clifton 8'#'Vivobarefoot Primus Lite II'#
        if activity == 'Walking':
            shoes = 'Altra Torin 5'
            #'Merrell Vego 2019'
    
    if activity == 'Running':
        for i in range(0,len(dr.dist_list)):
            #print(i)
            df = best_time_ws(dr.dist_list[i], df)
        
            df.to_csv(filename)
            
    
    #[ac_details['no'],ac_details['type'],ac_details['date'],ac_details['dist'],ac_details['time'],ac_details['shoes']] 
    
    #abbr_df = pd.DataFrame(columns=['abbr','type'])
    #abbr_row = pd.Series([ac_abbr,activity],index=abbr_df.columns)
    #mod_abbr = abbr_df.append(abbr_row,ignore_index=True)
    #mod_abbr.to_csv(r'temp-abbr.csv',index = False)

    #temp_df = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time','Shoes'])

    #row = [ac_abbr,activity,date, dist,full_string,shoes]#convert to details
    #a_row = pd.Series(row,index=temp_df.columns)
    #temp_df = temp_df.append(a_row,ignore_index=True)

    #if gpx_status == 'Y':
    #    temp_df.to_csv(r'temp-activities.csv',index=False)
    
        #print('pre_assess')    
    #    analyse.assess('temp-activities.csv',file_name)
        
    #    os.remove('temp-activities.csv')
    
    #else:
    #    temp_df.to_csv(r'{}'.format(file_name))

    #print('Processing email...')

    #try:
    #    import map_email_gen
    #    print('Sent on 1st attempt')
    #except:
    #    import map_email_gen

    #import map_email_gen
    
    ac_details = {'no': ac_abbr,
                  'type': activity,
                  'date':date,
                  'dist': dist,
                  'time': full_string,
                  'shoes': shoes,
                  'notes': notes}
    
    main_df = pd.DataFrame(data,columns=dr.cols)
    
    assess_main(main_df,df,ac_details)
        
    #if email_option == True:
    #    import email_functions
    
    #    settings = email_functions.load_settings()
    
    #    email_functions.activity_email(settings,ac_abbr,initials)

    print(f'Imported {ac_abbr}')
    
    sort_by_date()

    try:
        os.remove(FIT)
        print('FIT removed')
    except:
        print('No FIT file')
        
    try:
        os.remove(gpx)
        print('gpx removed')
    except:
        print('No gpx file')


    action_dict = {'timestamp': [get_timestamp()],
                   'page_type': ['upload'],
                   'detail': [ac_abbr],
                   'mode': ['user']}
    
    action_log(action_dict)
    
    #try:
    #    os.remove('temp-abbr.csv')
    #except:
    #    print('Complete!')  
    
    print('Complete')
    
def underscores_to_spaces(string):
    
    string = string.replace('_',' ')
    
    return(string)

import argparse

def import_from_args():
    
    parser = argparse.ArgumentParser()
    
    # Define the program description
    text = 'Imports activity from FIT or gpx or both.'

    parser = argparse.ArgumentParser(description=text)
    
    #define input options
    parser.add_argument("--FIT", "-f", help="FIT file from Garmin, with or without .FIT")
    
    parser.add_argument("--gpx", "-g", help="gpx file (from Strava), with or without .gpx")
    
    parser.add_argument("--activity", "-a", help='Optional: defaults to Walking/Running/Cycling depending on pace')
       
    parser.add_argument('--shoes', '-s', help='Optional: use {_} not { }')
    #have not added email option at this point
    parser.add_argument('--elevation', '-e', help='True/False, default True: can take time to import if FIT')
    
    parser.add_argument('--notes', '-n', help='Optional: use {_} not { }')
    
    parser.add_argument('--dev', '-d', help='Alternative: add dev or user switch to usage log; separate from uploading activity')
    
    #convert input options to function inputs
    args = parser.parse_args()
    
    if args.FIT:
        FIT = args.FIT
    else:
        FIT = 'NONE'
        
    if args.gpx:
        gpx = args.gpx
    else:
        gpx = 'NONE'
        
    if args.activity:
        activity = underscores_to_spaces(args.activity)
    else:
        activity = 'auto'
        
    #activity = 'Alpine Skiing'
    
    if args.shoes:
        shoes = underscores_to_spaces(args.shoes)
    else:
        shoes = 'default'
    
    if args.elevation:
        if any(t in args.elevation for t in ['T','t']):
            alt_option = True
        else:
            alt_option = False
    else:
        if any(f in str(args.elevation) for f in ['F','f']):
            alt_option = False
        else:
            alt_option = True
        
        
    if args.notes:
        notes = underscores_to_spaces(args.notes)
    else:
        notes = ''
        
    #notes = 'Val Thorens, with Dad & Paul'
        
    if args.dev:
        mode = args.dev
        action_dict = {'timestamp': [get_timestamp()],
                   'page_type': ['usage_set'],
                   'mode': [mode]}
        action_log(action_dict)    
    elif FIT == 'NONE' and gpx == 'NONE':
        print('Requires a --FIT or a --gpx file to import')
    else:
        
        activity_import(FIT=FIT, gpx=gpx, activity=activity, shoes=shoes, alt_option=alt_option, notes=notes)
    
#alas, I now have to actually run the script...
#import_from_args()
    
   

