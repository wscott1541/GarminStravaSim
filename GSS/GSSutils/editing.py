# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 09:03:26 2021

@author: WS
"""

import pandas as pd

import haversine
from math import sqrt
from datetime import datetime
import time

import os


from . import data_read as dr

from . import loading_modules as lm
# best_time_ws

#assess_main(main_df,gpx_df,ac_details
    
def nan_to_none(x):
    
    if str(x) == 'nan' or str(x) == 'NONE':
        x = ''
        
    return(x)

def format_url(x):
    
    if 'str' in str(type(x)):
        x = x.replace('_',' ')
        x = x[:1].upper() + x[1:]
        
    return(x)

def reset_distances(user_df,activity_number,column,new):
    
    location = user_df.loc[user_df['Activity number'] == activity_number].index.values[0]
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    
    filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.csv'.format(activity_number))
    
    a_df = pd.read_csv(r'{}'.format(filename))
    
    archive = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}_a.csv'.format(activity_number))
    
    a_df.to_csv(archive)
    
    cols = ['time', 'lat', 'lon', 'HR', 'distance', 'cadence', 'alt']
    cols = [c for c in cols if c in list(a_df.columns)]
    a_df = a_df[cols]
    
    distances = [0]
    
    lats = a_df['lat'].tolist()
    lons = a_df['lon'].tolist()
    alts = a_df['alt'].tolist()
    
    
    for i in range(1,len(a_df)):
        prev_lon = lons[i-1]
        prev_lat = lats[i-1]
        prev_alt = alts[i-1]
        
        lon, lat, alt = lons[i], lats[i], alts[i]
                
        delta_2D = haversine.haversine((prev_lat,prev_lon),(lat,lon)) * 1000
                    
        delta_alt = alt - prev_alt
                    
        distance_3D = sqrt((delta_2D ** 2) + (delta_alt ** 2))
                
        new = distances[-1] + distance_3D
        
        distances.append(new)
        
    a_df['distance'] = distances
    
    final_distance = distances[-1]
    
    activity = user_df.at[location,'Activity Type']
    
    a_df['time'] = a_df['time'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    
    times = {}
    
    if activity == 'Running':
        for i in dr.dist_list:
            if final_distance >= dr.dist_dict[i]:
                a_df = lm.best_time_ws(i, a_df)
        
                a_df.to_csv(r'{}'.format(filename))
            
                times[i] = lm.best_time_ws(i, a_df, True)
                
    a_df = a_df[cols+list(times.keys())]
                
    for i in dr.dist_list:
        user_df.at[location, i] = times.get(i) or 'NONE'
        
    user_df.at[location, 'Distance'] = round(final_distance/1000,2)
    
    notes = str(user_df.at[location, 'Notes'])
    a_df.to_csv(r'{}'.format(filename))
    
    if notes == 'nan':
        notes = ''
    else:
        notes = notes+'; '
        
    notes = notes + 'Altered gpx'
    
    user_df.at[location, 'Notes'] = notes
    
    times = a_df['time'].tolist()
    
    user_df.at[location, 'Date'] = times[0]
    
    duration = times[-1] - times[0]
    full_secs = duration.total_seconds()

    user_df.at[location, 'Time'] = time.strftime('%H:%M:%S',time.gmtime(full_secs))
    
    user_df.to_csv('activities.csv',index=False)
    
def download_as_csv(activity_number,suffix):
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    
    filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.csv'.format(activity_number))
    
    a_df = pd.read_csv(r'{}'.format(filename))
    
    def add_csv(x:str)->str:
        return x if x[-4:]=='.csv' else x+'.csv'
    
    if suffix == 'Download':
        output_filename = 'activity_' + str(activity_number)
        output_filename = add_csv(output_filename)
    elif suffix  in ['archive', 'original']:
        output_filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}_{}.csv'.format(activity_number, suffix))
    else:
         output_filename = add_csv(suffix)

    a_df.to_csv(r'{}'.format(output_filename))

    return output_filename        

def edit_prompt(user_df,column):
    
    if column == 'Shoes':
        
        s_df = user_df[['Date','Shoes']].sort_values(by='Date',ascending=False)
        s_df['Shoes'] = s_df['Shoes'].fillna('NONE')
        s_df = s_df.drop_duplicates(subset=['Shoes'],keep='first')
        shoes = s_df['Shoes'].tolist()
        shoes = list(filter(lambda x: x not in ['NONE', 'default'], shoes))
        
        def shoes_link(shoe):
            link = shoe.replace(' ','_')
            return f"<a href='{link}'>{shoe}</a>"
        
        text = '<br>'.join(list(map(shoes_link, shoes)))
        
    elif column == 'Download':
        text = """<a href='Download'>Download</a> or <a href='archive'>archive</a>
<br>or type the desired filename into the url bar
        """
    else:
        text = 'To amend, add to url with underscores in lieu of spaces'
    
    return text

def edit_field(user_df,activity_number,column,new):
    
    location = user_df.loc[user_df['Activity number'] == activity_number].index.values[0]

    allowed = ['Notes','Admin','Activity Type','Shoes']#At some point do type, but, for the moment, that contains a space

    column = format_url(column)

    if column in allowed:
        
        print(user_df[column].dtype)
        
        if '64' in str(user_df[column].dtype):
            user_df[column] = user_df[column].apply(lambda x: str(x))
        
        user_df[column] = user_df[column].apply(nan_to_none)
        
        new = format_url(new)
        
        user_df.at[location,column] = new
        
        user_df.to_csv('activities.csv', index = False)
        
        out = 'Edit complete'
        
    elif column == 'Reset':
        
        reset_distances(user_df,activity_number,column,new)
        
        out = 'File reset'
        
    elif column == 'Download':
        
        path = download_as_csv(activity_number,new)
        
        out = 'Downloaded to ' + path

    else:
        out = f'{column} not editable'
        
    return(out)

    
    