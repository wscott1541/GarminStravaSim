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
from dateutil import relativedelta

import pandas as pd
import numpy as np

challenges_dict = {'one_year': ['lejog','via_francigena'],
                   'n_years': ['custom_route']}

challenge_list = challenges_dict['one_year'] + challenges_dict['n_years']

#challenge_list = ['lejog','via_francigena','custom_route']

def translate_title(x):
    s = x.split('_')
    l = []
    for w in s:
        a = w[0].upper() + w[1:]
        l.append(a)

    l = ' '.join(l)
    
    return l

def pull_year(x):
    return(float(x[:4]))

def import_challenge_csv(filename):
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    file = os.path.join(fileDir, 'Challenges/{}.csv'.format(filename))
    
    data = pd.read_csv(file)
    df = pd.DataFrame(data)
    
    return (df)

def challenge_one_year(fig,year,user_df,c_df):
    
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
     

def one_year_challenge(year,user_df,activity_string):
    
    user_df = user_df[user_df['Activity Type'].isin(['Walking','Running','Hiking'])]
    
    c_df = import_challenge_csv(activity_string)
    
    challenge_dist = round(c_df.iloc[-1]['distance']/1000,2)
    
    title_string = translate_title(activity_string)
    
    fig = go.Figure(go.Scattermapbox(
    mode = "lines",
    name = f'{title_string}: {challenge_dist}km',
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
        fig = challenge_one_year(fig,y,user_df,c_df)
        
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

def challenge_n_years(fig,user_df,c_df):
            
    #year_df['cum_df'] = year_df['Distance'].cumsum()
    distance = user_df['Distance'].sum() * 1000
    
    #raise ValueError(distance)
    
    y_df = c_df[c_df['distance'] <= distance]
    
    #hover_t = '%{text}km<extra></extra>',
    #txt = round(y_df['distance']/1000,2)
    
    #if year == str(ts.year):    
    fig.add_trace(go.Scattermapbox(
        mode='lines',
        name='Covered: {}km'.format(round(user_df['Distance'].sum(),2)),
        lon=y_df['lon'],
        lat=y_df['lat'],
        line={'color': '#000000'},
        #customdata=lap_df[['dist_annot','time_annot']],
        hovertemplate='%{text}km<extra></extra>',#'<extra></extra>',
        text=round(y_df['distance']/1000,2),
        marker={'size': 10}#,
        #visible='legendonly'
        ))
    #else:
    #    fig.add_trace(go.Scattermapbox(
    #    mode='lines',
    #    name='{}: {}km'.format(year,round(year_df['Distance'].sum(),2)),
    #    lon=y_df['lon'],
    #    lat=y_df['lat'],
    #    line={'color': '#000000'},
    #    #customdata=lap_df[['dist_annot','time_annot']],
    #    hovertemplate='%{text}km<extra></extra>',#'<extra></extra>',
    #    text=round(y_df['distance']/1000,2),
    #    marker={'size': 10}
    #    visible='legendonly'
    #    ))
    
    return(fig)

def n_years_challenge(user_df,activity_string):
    
    user_df = user_df[user_df['Activity Type'].isin(['Walking','Running','Hiking'])]
    
    c_df = import_challenge_csv(activity_string)
    
    challenge_dist = round(c_df.iloc[-1]['distance']/1000,2)
    
    title_string = translate_title(activity_string)
    
    fig = go.Figure(go.Scattermapbox(
    mode = "lines",
    name = f'{title_string}: {challenge_dist}km',
    lon = c_df['lon'],
    lat = c_df['lat'],
    line = {'color':'#FF0000'},
    #customdata = ac_df[['dist_annot','time_annot']],
    hovertemplate = '%{text}km<extra></extra>',
    text = round(c_df['distance']/1000,2),
    marker = {'size': 10},
    showlegend = True))
    
    fig = challenge_n_years(fig,user_df,c_df)
        
    #lat_min = c_df['lat'].min()
    #lon_min = c_df['lon'].min()
    #lat_max = c_df['lat'].max() 
    #lon_max = c_df['lon'].max()
    
    #lon_mid = (lon_max + lon_min)/2
    #lat_mid = (lat_max + lat_min)/2
    
    covered_distance = user_df['Distance'].sum() * 1000
    c_df = c_df[c_df['distance']<covered_distance]
    final_lat = c_df['lat'].tolist()[-1]
    final_lon = c_df['lon'].tolist()[-1]
    
    fig.update_layout(mapbox_style="open-street-map")
    
    fig.update_layout(
        mapbox={'center':{'lon': final_lon, 'lat': final_lat},
                'zoom': 10})
    
    div = pio.to_html(fig,auto_play=False,full_html=False)
    
    return(div)

def challenge(year,user_df,activity_string):
    
    if activity_string in challenges_dict['one_year']:
        div = one_year_challenge(year,user_df,activity_string)
        
    elif activity_string in challenges_dict['n_years']:
        div = n_years_challenge(user_df,activity_string)
        
    else:
        div = "This ain't no challenge"
        
    return div


def one_year_challenge_update(ac_no,user_df,activity_string):
    
    user_df = user_df[user_df['Activity Type'].isin(['Running','Walking','Hiking'])]
    
    date = dr.ac_detail(ac_no,'Date')
    
    year = str(date[:4])
    
    if 'str' not in str(type(year)):
        year = str(year)
    
    start = datetime.strptime(year,'%Y')
    
    user_df['Date'] = user_df['Date'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    
    user_df = user_df[user_df['Date'] >= start]
        
    c_df = import_challenge_csv(activity_string)
    
    if 'waymark' in list(c_df.columns):
        c_df = c_df[c_df['waymark']==c_df['waymark']]
        missing = False
    else:
        c_df['waymark'] = ['Start'] + [np.nan]*(len(c_df)-2) + ['Finish']
        missing = True  
    
    pre_dist = 1000 * user_df[user_df['Date'] < date]['Distance'].sum()
    post_dist = 1000 * user_df[user_df['Date'] <= date]['Distance'].sum()
    
    pre_loc = c_df[c_df['distance'] <= pre_dist]['waymark'].tolist()[-1]
    post_loc = c_df[c_df['distance'] <= post_dist]['waymark'].tolist()[-1]
    
    
    if post_dist < c_df['distance'].tolist()[-1]:
        place_distance = c_df[c_df['waymark']==post_loc]['distance'].tolist()[0]
        next_place = c_df[c_df['distance']>place_distance]['waymark'].tolist()[0]
        next_dist = c_df[c_df['waymark']==next_place]['distance'].tolist()[0]
    else:
        place_distance = c_df['distance'].tolist()[-1]
        next_place = False
        next_dist = np.nan
        last_place = c_df['waymark'].tolist()[-1]
    
    place_distance = round(place_distance/1000,1)
    next_dist = round(next_dist/1000,1)
    
    if not next_place:
        last_text = f'You reached <b>{last_place}</b>!'
    elif pre_loc != post_loc:
        last_text = f'You reached <b>{post_loc}</b>!'
    else:
        last_text = f'Last waymark: {pre_loc}, {place_distance}km'
        
    if next_place:
        next_text = f'Next waymark: {next_place}, {next_dist}km'
    else:
        next_text = f'{place_distance}km'
        
    title_string = translate_title(activity_string)
    
    
    html = f"""<b>{title_string}</b>: {round(post_dist/1000,2)}km
<br>{last_text}
<br>{next_text}"""

    if missing:
        html = ''

    return(html)

def n_years_challenge_update(ac_no,user_df,activity_string):
    
    user_df = user_df[user_df['Activity Type'].isin(['Running','Walking','Hiking'])]
    
    date = dr.ac_detail(ac_no,'Date')
    
    #year = str(date[:4])
    
    #if 'str' not in str(type(year)):
    #    year = str(year)
    
    #start = datetime.strptime(year,'%Y')
    
    user_df['Date'] = user_df['Date'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    
    #user_df = user_df[user_df['Date'] >= start]
        
    c_df = import_challenge_csv(activity_string)
    
    if 'waymark' in list(c_df.columns):
        c_df = c_df[c_df['waymark']==c_df['waymark']]
        missing = False
    else:
        c_df['waymark'] = ['Start'] + [np.nan]*(len(c_df)-2) + ['Finish']
        missing = True  
    
    pre_dist = 1000 * user_df[user_df['Date'] < date]['Distance'].sum()
    post_dist = 1000 * user_df[user_df['Date'] <= date]['Distance'].sum()
    
    pre_loc = c_df[c_df['distance'] <= pre_dist]['waymark'].tolist()[-1]
    post_loc = c_df[c_df['distance'] <= post_dist]['waymark'].tolist()[-1]
    
    
    if post_dist < c_df['distance'].tolist()[-1]:
        place_distance = c_df[c_df['waymark']==post_loc]['distance'].tolist()[0]
        next_place = c_df[c_df['distance']>place_distance]['waymark'].tolist()[0]
        next_dist = c_df[c_df['waymark']==next_place]['distance'].tolist()[0]
    else:
        place_distance = c_df['distance'].tolist()[-1]
        next_place = False
        next_dist = np.nan
        last_place = c_df['waymark'].tolist()[-1]
    
    place_distance = round(place_distance/1000,1)
    next_dist = round(next_dist/1000,1)
    
    if not next_place:
        last_text = f'You reached <b>{last_place}</b>!'
    elif pre_loc != post_loc:
        last_text = f'You reached <b>{post_loc}</b>!'
    else:
        last_text = f'Last waymark: {pre_loc}, {place_distance}km'
        
    if next_place:
        next_text = f'Next waymark: {next_place}, {next_dist}km'
    else:
        next_text = f'{place_distance}km'
        
    title_string = translate_title(activity_string)
    
    
    html = f"""<b>{title_string}</b>: {round(post_dist/1000,2)}km
<br>{last_text}
<br>{next_text}"""

    if missing:
        html = ''

    return(html)

def challenge_update(ac_no,user_df,activity_string):
    
    if activity_string in challenges_dict['one_year']:
        div = one_year_challenge_update(ac_no,user_df,activity_string)
        
    elif activity_string in challenges_dict['n_years']:
        div = n_years_challenge_update(ac_no,user_df,activity_string)
        
    else:
        div = "This ain't no challenge"
        
    return div


def find_one_year_waymark_dates(challenge,user_df,year):
    
    c_df = import_challenge_csv(challenge)
    
    user_df = user_df[user_df['Activity Type'].isin(['Running','Walking','Hiking'])]
    user_df['year'] = user_df['Date'].apply(pull_year)
    user_df = user_df[user_df['year']==year]
    
    def cumsum(l):
        a = [0]
        for i in l:
            a.append(i+a[-1])
        a = a[1:]
        return a
    
    user_df['distance_sum'] = cumsum(user_df['Distance'].tolist())
    user_df['distance_sum'] = user_df['Distance'].cumsum() * 1000
    
    
    c_df = c_df[-pd.isna(c_df['waymark'])]
    
    start_date = datetime.strptime(f'{int(year)}-01-01','%Y-%m-%d')
    days = [datetime.strftime(start_date+relativedelta.relativedelta(days=i),'%Y-%m-%d') for i in range(365)]
        
    if days[-1] != f'{int(year)}-12-31':
        days += [f'{int(year)}-12-31']
    
    
    waymarks = {k: v for k,v in zip(c_df['waymark'],c_df['distance'])}
    
    waymark_checks = {}

    for place, distance in waymarks.items():
        if place == c_df['waymark'].tolist()[0]:
            waymark_checks[c_df['waymark'].tolist()[0]] = '1 Jan'
        else:
            
            #p_df = user_df[-user_df['distance_sum'] > distance]#.reset_index(drop=True)
            
            p_df = user_df.copy().reset_index(drop=True)
            final_distance = p_df.at[len(p_df)-1,'distance_sum']
            p_df['filter'] = p_df['distance_sum'].apply(lambda x: 1 if x > distance else 0)
            p_df = p_df[p_df['filter']==1]
            p_df = p_df.reset_index(drop=True)
            
            #if str(year) == '2021':
            #    raise ValueError(year,place, distance, p_df, user_df['distance_sum'].tolist()[-1],
            #                     user_df['distance_sum'].tolist()[-1] > distance,
            #                     user_df['distance_sum'].tolist()[0] > distance,
            #                     p_df.at[len(p_df)-1,'Date'])
            
                #raise ValueError(final_distance)
            
            if not p_df.empty and final_distance > distance:
                date = p_df.at[0,'Date']
                date = str(date)[:10]
                date = datetime.strptime(date, '%Y-%m-%d')
                date = datetime.strftime(date, '%d %b' )
                waymark_checks[place] = date
            
    #raise ValueError (year, waymark_checks)    
     
    return waymark_checks

def one_year_waymark_table(challenge,user_df):
    
    user_df['year'] = user_df['Date'].apply(pull_year)
    start_year = int(user_df['year'].min())
    end_year = int(user_df['year'].max()) + 1
    
    years = {}
    
    for yyyy in range(start_year, end_year):
        
        years[str(yyyy)] = find_one_year_waymark_dates(challenge,user_df,yyyy)
        
    c_df = import_challenge_csv(challenge)
    c_df = c_df[-pd.isna(c_df['waymark'])]
    
    waymarks = c_df['waymark'].tolist()
    
    w_df = pd.DataFrame()
    w_df['Waymark'] = waymarks
    w_df['Distance'] = [f'{round(d/1000,2)}km' for d in c_df['distance'].tolist()]
    
    for y in years:
        w_df[y] = w_df['Waymark'].apply(lambda x: years[y].get(x) or '')
        
    table = '<tr>'
    
    for k in w_df.columns.tolist():
        table += f'<th>{k}</th>'
    
    table += '</tr>'

    for i in range(0,len(w_df)):
        
        table += '<tr>'
        
        for k in w_df.columns.tolist():
            
            table += f'<td>{w_df.at[i,k]}</td>'
            
        table += '</tr>'
    
    return table  

def n_years_waymark_table(challenge,user_df):
    
    user_df = user_df[user_df['Activity Type'].isin(['Running','Walking','Hiking'])]    
        
    c_df = import_challenge_csv(challenge)
    c_df = c_df[-pd.isna(c_df['waymark'])]
    
    waymarks_list = c_df['waymark'].tolist()
    
    waymarks = {k: v for k,v in zip(c_df['waymark'],c_df['distance'])}
    
    waymark_checks = {}

    for place, distance in waymarks.items():
        if place == c_df['waymark'].tolist()[0]:
            date = user_df.at[0,'Date']
            date = str(date)[:10]
            date = datetime.strptime(date, '%Y-%m-%d')
            date = datetime.strftime(date, '%d %b %Y' )
            waymark_checks[c_df['waymark'].tolist()[0]] = date
        else:
            
            #p_df = user_df[-user_df['distance_sum'] > distance]#.reset_index(drop=True)
            
            p_df = user_df.copy().reset_index(drop=True)
            p_df['distance_sum'] = p_df['Distance'].cumsum() * 1000
            final_distance = user_df['Distance'].sum() * 1000#p_df.at[len(p_df)-1,'distance_sum']
            p_df['filter'] = p_df['distance_sum'].apply(lambda x: 1 if x > distance else 0)
            #raise ValueError(p_df.tail())
            p_df = p_df[p_df['filter']==1]
            #raise ValueError(p_df[['Date','distance_sum']].tail())
            p_df = p_df.reset_index(drop=True)
            
            #if str(year) == '2021':
            #    raise ValueError(year,place, distance, p_df, user_df['distance_sum'].tolist()[-1],
            #                     user_df['distance_sum'].tolist()[-1] > distance,
            #                     user_df['distance_sum'].tolist()[0] > distance,
            #                     p_df.at[len(p_df)-1,'Date'])
            
                #raise ValueError(final_distance)
            
            if not p_df.empty and final_distance > distance:
                date = p_df.at[0,'Date']
                date = str(date)[:10]
                date = datetime.strptime(date, '%Y-%m-%d')
                date = datetime.strftime(date, '%d %b %Y' )
                waymark_checks[place] = date
    
    w_df = pd.DataFrame()
    w_df['Waymark'] = waymarks_list
    w_df['Distance'] = [f'{round(d/1000,2)}km' for d in c_df['distance'].tolist()]
    
    w_df['Date'] = w_df['Waymark'].apply(lambda x: waymark_checks.get(x) or '')
        
    COLUMNS = w_df.columns.tolist()
    
    col_style = {COLUMNS[0]: 'style="width: 140px; text-align: left;"',
                 COLUMNS[1]: 'style="width: 100px; text-align: center;"',
                 COLUMNS[2]: 'style="width: 100px; text-align: center;"'}
    
    table = '<tr>'
    
    for k in COLUMNS:
        table += f'<th>{k}</th>'
    
    table += '</tr>'

    for i in range(0,len(w_df)):
        
        table += '<tr>'
        
        for k in COLUMNS:
            
            style = col_style.get(k) or ''
            
            table += f'<td {style}>{w_df.at[i,k]}</td>'
            
        table += '</tr>'
    
    return table 

def waymark_table(challenge,user_df):
    
    if challenge in challenges_dict['one_year']:
        div = one_year_waymark_table(challenge,user_df)
        
    elif challenge in challenges_dict['n_years']:
        div = n_years_waymark_table(challenge,user_df)
        
    else:
        div = "This ain't no challenge"
        
    return div
    

def one_year_plot_challenge_linear_progress(challenge,user_df,year):
    
    c_df = import_challenge_csv(challenge)
    
    user_df = user_df[user_df['Activity Type'].isin(['Running','Walking','Hiking'])]
    
    full_distance = c_df.at[len(c_df)-1,'distance']/1000
    
    challenge_name = translate_title(challenge)
    
    fig = go.Figure()
    
    fig.add_trace(
            go.Scatter(
                mode='lines',
                name=challenge_name,
                x=[1,364],
                y=[0,full_distance],
                line={'color': 'red'},
                #hovertemplate = hover_t,
                #hoverinfo = 'skip',
                showlegend = True
                ))
    
    user_df['year'] = user_df['Date'].apply(pull_year)
    user_df['Date'] = user_df['Date'].apply(lambda x: x[:10])
    user_df = user_df[['Date','Distance','year']].groupby('Date').sum().reset_index()
    user_df['year'] = user_df['Date'].apply(pull_year)
    start_year = int(user_df['year'].min())
    user_df = user_df.drop(columns=['year'])
    
    for yyyy in range(start_year,year+1):
        start_date = datetime.strptime(f'{int(yyyy)}-01-01','%Y-%m-%d')
        days = [datetime.strftime(start_date+relativedelta.relativedelta(days=i),'%Y-%m-%d') for i in range(365)]
        
        if days[-1] != f'{yyyy}-12-31':
            days += [f'{yyyy}-12-31']
            
        if yyyy == year:
            days = [d for d in days if d <= ts.today_string]
        
        y_df = pd.DataFrame.from_dict({'Date': days})
        
        y_df = pd.merge(y_df,user_df,how='left',on='Date')
        
        y_df['Distance'] = y_df['Distance'].fillna(0)
        
        y_df['Distance Covered'] = y_df['Distance'].cumsum().fillna(0)
        
        y_df['index'] = [x for x in range(1,len(y_df)+1)]
        
        if yyyy == year:
            fig.add_trace(go.Scatter(
        mode='lines',
        name='{}: {}km'.format(year,round(y_df['Distance'].sum(),2)),
        x=y_df['index'],
        y=y_df['Distance Covered'],
        line={'color': '#000000'},
        marker={'size': 10}#,
        #visible='legendonly'
        ))
        else:
            fig.add_trace(go.Scatter(
        mode='lines',
        name='{}: {}km'.format(yyyy,round(y_df['Distance'].sum(),2)),
        x=y_df['index'],
        y=y_df['Distance Covered'],
        line={'color': '#000000'},
        marker={'size': 10},
        visible='legendonly'
        ))
    
    div = pio.to_html(fig,auto_play=False,full_html=False)
    
    return(div)

def plot_challenge_linear_progress(challenge,user_df,year):
    
    if challenge in challenges_dict['one_year']:
        div = one_year_plot_challenge_linear_progress(challenge,user_df,year)
        
    elif challenge in challenges_dict['n_years']:
        div = "Nothin' yet"
        
    else:
        div = "This ain't no challenge"
        
    return div

def challenge_summary(challenge,user_df,year):
    
    c_df = import_challenge_csv(challenge)
    user_df = user_df[user_df['Activity Type'].isin(['Running','Walking','Hiking'])]
    
    user_df['year'] = user_df['Date'].apply(pull_year)
    start_year = int(user_df['year'].min())
    
    waypoints = {}
    years = []
    
    for y in range(start_year,year+1):
        
        y_df = user_df[user_df['year']==y]
        distance_covered = y_df['Distance'].fillna(0).sum() * 1000
        
        y_c_df = c_df[c_df['distance'] < distance_covered]
        
        y_c_df = y_c_df[-pd.isna(y_c_df['waymark'])]
        
        last_point = y_c_df['waymark'].tolist()[-1]
        last_dist = y_c_df['distance'].tolist()[-1]
        
        waypoints[str(y)] = last_point
        
        waypoints[str(y)+'_dist'] = round(last_dist/1000, 2)
        
        years.append(y)
    
    years.reverse()
    
    p = []
    
    for y in years:
        try:
            p.append(f'{str(y)}: {waypoints[str(y)]} @ {waypoints[str(y)+"_dist"]}km')
        except:
            raise ValueError(year,
                             str(y),type(y),
                             waypoints)
        
    p = '<br>'.join(p)
    
    return p

