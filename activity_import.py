# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:18:10 2020

@author: WS
"""

import os

import pandas as pd

from fitparse import FitFile

from today_string import today_string, day, month, year

from datetime import datetime, timedelta
import time

import gpxpy

import haversine
from math import sqrt

import data_read as dr

import analyse

conversion = 180 / (2 ** 31)

def activity_import(FIT='NONE',gpx='NONE',activity='auto',shoes='default'):

    #set-up
    initials = dr.pull_initials()
    
    if ('FIT' not in FIT) and (FIT != 'NONE'):
        FIT = FIT + '.FIT'
    
    if ('gpx' not in gpx) and (gpx != 'NONE'):
        gpx = gpx + '.gpx'
        
    if gpx != 'NONE':
        
        name_options = 'ABCDE'
        
        available_options = []
        
        latest_name = dr.latest_activity(initials)
        
        for i in range(0,len(name_options)):
            if  f'{name_options[i]}{year}{month}{day}' != latest_name:
                available_options.append(f'{name_options[i]}{year}{month}{day}')
        
        ac_abbr = available_options[0]
    else:
        pos = FIT.find('.FIT')
        
        ac_abbr = FIT[:pos] 
        
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
        lat_break_checks = []
        lon_breaks = []
        lon_break_checks = []

        for i in range(0,len(timestamps)):
    
            if activity != 'Cardio':
                try:
                    lat = latitudes[i] * conversion
                except:
                    if len(lat_breaks) == 0:
                        lat_breaks.append(latitudes[i-1] * conversion)
                    elif lat_break_checks[-1] == i - 1:
                        here = 'junk'
                    else:
                        lat_breaks = [latitudes[i-1] * conversion]
                        lat_break_checks.append(i)
        
                    lat = lat_breaks[0]

                try:
                    lon = longitudes[i] * conversion
                except:
                    if len(lon_breaks) == 0:
                        lon_breaks.append(longitudes[i-1] * conversion)
                    elif lon_break_checks[-1] == i - 1:
                        here = 'junk'
                    else:
                        lon_breaks = [longitudes[i-1] * conversion]
                        lon_break_checks.append(i)    
        
                    lon = lon_breaks[0]
                
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
            
            stop = 0
        except:
            stop = 1
            print('Early break')

        df = pd.DataFrame(columns=['lon','lat','alt','time','distance','HR'])
        #df = pd.DataFrame(columns=['lon','lat','alt'])

        distances.append(0)

        hrs = []
        
        print('Matching FIT to gpx')

        if stop == 0:
            for i in range(0,len(data)):
                #print(i)
                lon = data[i].longitude
                lat = data[i].latitude
                alt = data[i].elevation
        
                time_str = str(data[i].time)[:19]
                time_dt = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
                timestamps.append(time_dt)
        
                hr_found = False
        
                #while hr_found == False:
            
                for n in range(0,len(fit_ts)):
                    if time_dt == fit_ts[n] and hr_found == False:
                        hrs.append(fit_hr[n])
                        #print(f'{i}/{len(fit_ts)}',fit_hr[n])
                        hr_found = True
                #if n == len(fit_ts) - 1:
                #    hr_found = True
                #    hrs.append(hrs[-1])
                #    print(f'HR {i} not found')
                
                    #print('HR found: ',time_dt)

                hr = hrs[-1]

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

    filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.csv'.format(ac_abbr))
    
    df.to_csv(r'{}'.format(filename))
        
    #end of activity imports

    file_name = "{}activities.csv".format(initials)
    
    data = pd.read_csv(r'{}'.format(file_name))
    
    gpx_status = dr.pull_gpx_status(initials)
    
    if gpx_status == 'Y':
        archive = pd.DataFrame(data, columns= dr.cols)
    else:
        archive = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time'])    

    #initial archiving
    archive = pd.DataFrame(data)
    archname = os.path.join(fileDir, 'Archive.gitignore/{}{}'.format(today_string,file_name))
    archive.to_csv(r'{}'.format(archname), index = False)

    date = timestamps[0]# + timedelta(hours=1)
    dist = round((distances[-1]/1000),2)
    full_td = timestamps[-1] - timestamps[0]
    full_secs = full_td.total_seconds()
    full_string = time.strftime('%H:%M:%S',time.gmtime(full_secs))

    pace = full_secs/dist

    if activity == 'auto':
        if pace < 181:
            activity = 'Cycling'
            #shoes = 'NONE'
        if pace >= 181 and pace <= 570:
            activity = 'Running'
            #shoes = 'Kalenji Run Support Red'
            #shoes = 'Hoka One One Clifton 6'
        if pace > 570:
            activity = 'Walking'
            #shoes = 'Merrell Vego 2019'
    if activity == 'auto':
        if pace < 181:
            activity = 'Cycling'
        if pace >= 181 and pace <= 570:
            activity = 'Running'
        if pace > 570:
            activity = 'Walking'
            
    if activity == 'Cardio':
        shoes = 'NONE'
        
    if shoes == 'default':
        if activity == 'Cycling':
            shoes = 'NONE'
        if activity == 'Running':
            shoes = 'Hoka One One Clifton 6'
        if activity == 'Walking':
            shoes = 'Merrell Vego 2019'
    
    
    abbr_df = pd.DataFrame(columns=['abbr','type'])
    abbr_row = pd.Series([ac_abbr,activity],index=abbr_df.columns)
    mod_abbr = abbr_df.append(abbr_row,ignore_index=True)
    mod_abbr.to_csv(r'temp-abbr.csv',index = False)

    temp_df = pd.DataFrame(data, columns= ['Activity number','Activity Type','Date','Distance','Time','Shoes'])

    row = [ac_abbr,activity,date, dist,full_string,shoes]
    a_row = pd.Series(row,index=temp_df.columns)
    temp_df = temp_df.append(a_row,ignore_index=True)

    if gpx_status == 'Y':
        temp_df.to_csv(r'temp-activities.csv',index=False)
    
        #print('pre_assess')    
        analyse.assess('temp-activities.csv',file_name)
        
        os.remove('temp-activities.csv')
    
    else:
        temp_df.to_csv(r'{}'.format(file_name))

    #print('Processing email...')

    #try:
    #    import map_email_gen
    #    print('Sent on 1st attempt')
    #except:
    #    import map_email_gen

    #import map_email_gen
    
    import email_functions
    
    settings = email_functions.load_settings()
    
    email_functions.activity_email(settings,ac_abbr,initials)

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

    try:
        os.remove('temp-abbr.csv')
    except:
        print('Complete!')  
        
#activity_import(FIT='ACRB1018')
#activity_import(FIT='ACTG2250',activity='Cardio')
#activity_import(FIT='ACVH5024',activity='Cardio')
#activity_import(FIT='B14H1013',activity='Cardio')
#activity_import(FIT='B16H2648',activity='Cardio')
#activity_import(FIT='B18H3619',activity='Cardio')
#activity_import(FIT='B1BH0531',activity='Cardio')
activity_import(FIT='B1EB0152')