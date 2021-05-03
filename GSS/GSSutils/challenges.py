#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 16:38:55 2021

@author: willscott
"""

import os

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

from . import data_read as dr
from . import basic_functions as bf
from . import today_string as ts

from datetime import datetime, timedelta

import pandas as pd

def import_challenge_csv(filename):
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    file = os.path.join(fileDir, 'Challenges/{}.csv'.format(filename))
    
    data = pd.read_csv(file)
    df = pd.DataFrame(data)
    
    return (df)

def lejog_one_year(fig,year,user_df,c_df):
    
    if 'str' not in str(type(year)):
        year = str(year)
        
    if year == 2020:
        days_in_year = 365
    else:
        days_in_year = 364
    
    start = datetime.strptime(year,'%Y')
    end = start + timedelta(days=days_in_year)
    
    user_df['Date'] = user_df['Date'].apply(bf.convert_time)
    
    year_df = user_df[user_df['Date'] >= start]
    year_df = year_df[year_df['Date'] < end]
        
    #year_df['cum_df'] = year_df['Distance'].cumsum()
    distance = year_df['Distance'].sum() * 1000
    
    #raise ValueError(distance)
    
    y_df = c_df[c_df['distance'] <= distance]
    
    #hover_t = '%{text}km<extra></extra>',
    #txt = round(y_df['distance']/1000,2)
    
    if year == str(ts.year):    
        fig.add_trace(go.Scattermapbox(
        mode='lines',
        name='{}: {}km'.format(year,round(year_df['Distance'].sum(),2)),
        lon=y_df['lon'],
        lat=y_df['lat'],
        line={'color': '#000000'},
        #customdata=lap_df[['dist_annot','time_annot']],
        hovertemplate='%{text}km<extra></extra>',#'<extra></extra>',
        text=round(y_df['distance']/1000,2),
        marker={'size': 10}#,
        #visible='legendonly'
        ))
    else:
        fig.add_trace(go.Scattermapbox(
        mode='lines',
        name='{}: {}km'.format(year,round(year_df['Distance'].sum(),2)),
        lon=y_df['lon'],
        lat=y_df['lat'],
        line={'color': '#000000'},
        #customdata=lap_df[['dist_annot','time_annot']],
        hovertemplate='%{text}km<extra></extra>',#'<extra></extra>',
        text=round(y_df['distance']/1000,2),
        marker={'size': 10},
        visible='legendonly'
        ))
    
    return(fig)
     

def lejog(year,user_df):
    
    user_df = user_df[user_df['Activity Type'].isin(['Walking','Running','Hiking'])]
    
    c_df = import_challenge_csv('lejog')
    
    lejog_dist = round(c_df.iloc[-1]['distance']/1000,2)
    
    fig = go.Figure(go.Scattermapbox(
    mode = "lines",
    name = f'LEJOG: {lejog_dist}km',
    lon = c_df['lon'],
    lat = c_df['lat'],
    line = {'color':'#FF0000'},
    #customdata = ac_df[['dist_annot','time_annot']],
    hovertemplate = '%{text}km<extra></extra>',
    text = round(c_df['distance']/1000,2),
    marker = {'size': 10},
    showlegend = True))
    
    for i in range(0,int(year)-2017+1):
        y = round(float(year) - i)
        fig = lejog_one_year(fig,y,user_df,c_df)
        
    lat_min = c_df['lat'].min()
    lon_min = c_df['lon'].min()
    lat_max = c_df['lat'].max() 
    lon_max = c_df['lon'].max()
    
    lon_mid = (lon_max + lon_min)/2
    lat_mid = (lat_max + lat_min)/2
    
    fig.update_layout(mapbox_style="open-street-map")
    
    fig.update_layout(
        mapbox={'center':{'lon': lon_mid, 'lat': lat_mid},
                'zoom': 4.5})
    
    div = pio.to_html(fig,auto_play=False,full_html=False)
    
    return(div)
        

def lejog_update(ac_no,user_df):
    
    user_df = user_df[user_df['Activity Type'].isin(['Running','Walking'])]
    
    date = dr.ac_detail(ac_no,'Date')
    
    year = str(date[:4])
    
    if 'str' not in str(type(year)):
        year = str(year)
    
    start = datetime.strptime(year,'%Y')
    
    user_df['Date'] = user_df['Date'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    
    user_df = user_df[user_df['Date'] >= start]
        
    c_df = import_challenge_csv('lejog')
    
    c_df = c_df[c_df['waymark']==c_df['waymark']]
    
    pre_dist = 1000 * user_df[user_df['Date'] < date]['Distance'].sum()
    post_dist = 1000 * user_df[user_df['Date'] <= date]['Distance'].sum()
    
    pre_loc = c_df[c_df['distance'] <= pre_dist]['waymark'].tolist()[-1]
    post_loc = c_df[c_df['distance'] <= post_dist]['waymark'].tolist()[-1]
    
    place_distance = c_df[c_df['waymark']==post_loc]['distance'].tolist()[0]
    next_place = c_df[c_df['distance']>place_distance]['waymark'].tolist()[0]
    next_dist = c_df[c_df['waymark']==next_place]['distance'].tolist()[0]
    
    place_distance = round(place_distance/1000,1)
    next_dist = round(next_dist/1000,1)
    
    if pre_loc != post_loc:
        last_text = f'You reached <b>{post_loc}<b>!'
    else:
        last_text = f'Last waymark: {pre_loc},{place_distance}km'
        
    next_text = f'Next waymark: {next_place}, {next_dist}km'
    
    html = f"""<b>LEJOG</b>: {round(post_dist/1000,2)}km
<br>{last_text}
<br>{next_text}"""

    return(html)
    
