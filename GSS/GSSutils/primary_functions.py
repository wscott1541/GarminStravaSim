#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:22:17 2020

@author: WS
"""

import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
#pio.to_html(fig,auto_play=False,full_html=False)

from . import today_string as ts
today_string = ts.today_string
#print(today_string)
year = ts.year
month = ts.month
day = ts.day
y_day_string = ts.y_day_string

from . import analyse

import json
#print(day)

from datetime import datetime, timedelta
from dateutil import relativedelta

from math import pi

from . import data_read as dr

from . import mapper
#tmb_test = mapper.tmb_test
osm_map = mapper.plot_osm_map

from . import basic_functions as bf

import os
import base64

import numpy as np
import pandas as pd

from time import time

def populate_arrays(m,yyyy,month_dates,curr_vals):
    lim = bf.month_length(m,yyyy)
    
    if month_dates[-1] < lim:
        month_dates.append((month_dates[-1]) + 1)
        curr_vals.append(curr_vals[-1])
    
    count = 0
    i = 0      
    
    while i < lim:
        if month_dates[i] == month_dates[-1] and month_dates[i] != lim:
            month_dates.append(i+1-count)
            curr_vals.append(curr_vals[-1])
        elif month_dates[i] == month_dates[i+1]:
            count += 1
            lim += 1
        elif month_dates[i + 1] != i + 1 - count:
            month_dates.insert(i + 1,i + 1 - count)
            curr_vals.insert(i + 1,curr_vals[i])  
        i += 1
        
def duration_sum(m,yyyy,activity,user_df):
    dates = user_df['Date'].tolist()
    times = user_df['Time'].tolist()
    types = user_df['Activity Type'].tolist()
    
    mins = []
    
    for i in range(0,len(times)):
        time_string = str(times[i])
        minutes = bf.stringtime_to_floatminute(time_string)
        mins.append(minutes)
    
    plot_mins = [0]
    month_dates = [0]
    
    if activity == 'All':
        activity = 'i'
    
    for i in range(0,len(dates)):
        if bf.date_string(m,yyyy) in str(dates[i]) and activity in types[i]:
            times = plot_mins[-1] + mins[i]
            plot_mins.append(times)
            day_strf = datetime.strptime(dates[i],'%Y-%m-%d %H:%M:%S')
            day_strp = datetime.strftime(day_strf,'%d')
            month_dates.append(float(day_strp))
            #month_dates.append(float(dates[i][-2:]))
            
    populate_arrays(m,yyyy,month_dates,plot_mins)
    
    #error message?
    return(month_dates,plot_mins)

'''
def distance_sum(m,yyyy,activity,user_df):#can add 'All'
    
    dates = user_df['Date'].tolist()
    types = user_df['Activity Type'].tolist() 
    distances = user_df['Distance'].tolist()

    sum_distances = [0]
    month_dates = [0]
    
    if activity == 'All':
        activity = 'i'
    
    for i in range(0,len(dates)):
        if bf.date_string(m,yyyy) in dates[i] and activity in types[i]:
            dist = round(sum_distances[-1] + float(distances[i]),2)
            sum_distances.append(dist)
            month_dates.append(float(dates[i][-2:]))
    
    populate_arrays(m,yyyy,month_dates,sum_distances)
    
    #error message?
    return(month_dates,sum_distances)
'''

def month_dist_sum(m,yyyy,activity,user_df):#can add 'All'
    sum_distances = [0]
    month_dates = [0]
    
    user_df = user_df.loc[user_df['Activity Type'] == activity]
    
    dates = user_df['Date'].tolist()
    distances = user_df['Distance'].tolist()
    
    if activity == 'All':
        activity = 'i'
    
    for i in range(0,len(dates)):
        if bf.date_string(m,yyyy) in str(dates[i]):
            dist = round(sum_distances[-1] + float(distances[i]),2)
            sum_distances.append(dist)
            day_strf = datetime.strptime(dates[i],'%Y-%m-%d %H:%M:%S')
            day_strp = datetime.strftime(day_strf,'%d')
            month_dates.append(float(day_strp))
    
    populate_arrays(m,yyyy,month_dates,sum_distances)
    
    #print(month_dates)
    
    #error message?
    return(month_dates,sum_distances)

def plot_month_previous_distances(m,yyyy,activity,user_df):
    curr_month_dates, curr_sum_distances = month_dist_sum(m,yyyy,activity,user_df)
    
    if activity == 'All':
        activity = 'i'
        title_activity = 'All'
    else:
        title_activity = activity
    
    if m == 1:
        new_year = yyyy - 1
        prev_month = 12
    else:
        new_year = yyyy
        prev_month = m - 1
    prev_month_dates, prev_sum_distances = month_dist_sum(prev_month,new_year,activity,user_df)
    
    junk_month_dates,prev_mins = duration_sum(prev_month,new_year,activity,user_df)
    prev_annot = '{} {}: {}km in {} '.format(bf.month_caller(prev_month),new_year,round(prev_sum_distances[-1],2),bf.floatminute_to_stringtime(prev_mins[-1]))
    
    try:
        junk_month_dates_two,curr_mins = duration_sum(m,yyyy,activity,user_df)
        cm_string = bf.floatminute_to_stringtime(curr_mins[-1])
    except:
        cm_string = 'NOT FOUND'
    curr_annot = '{} {}: {}km in {} '.format(bf.month_caller(m),yyyy,round(curr_sum_distances[-1],2),cm_string)
    
    title = '{} distances in {} {} and {} {}'.format(title_activity, bf.month_caller(prev_month),new_year,bf.month_caller(m),yyyy)
    
    fig,ax = plt.subplots()
    plt.plot(prev_month_dates, prev_sum_distances,color='blue',label = prev_annot)
    #plt.text(prev_month_dates[-2],prev_sum_distances[-1],prev_annot,horizontalalignment='right')
    plt.plot(curr_month_dates, curr_sum_distances,color='red', label = curr_annot)
    #plt.text(curr_month_dates[-2],curr_sum_distances[-1],curr_annot,horizontalalignment='right')
    ax.legend();
    plt.title(title)
    
def order_date_vals(days):
    vals = [0]
    
    count = -1
    
    for i in range(1,len(days)):
        #print('d',i,': ',days[i])
        #print('d',i-1,': ',days[i-1])
        if days[i] == days[i-1]:
            count += 1
        vals.append(i-count)
    
    return(vals)

def populate_list(start_date,end_date,days,vals):
    
    #if days[-1] < lim:
    #    days.append((days[-1]) + 1)
    #    vals.append(vals[-1])
    
    lim_str = str(end_date - start_date)
    pos = lim_str.find(' ')
    n = lim_str[:pos]
    lim = round(float(n))
    
    count = 0
    i = 0      
    
    while i < lim:
        a = start_date + timedelta(days=(i+1))
        b = start_date + timedelta(days=(i+1-count))
        if days[i] == days[-1] and days[i] != end_date:
            days.append(b)
            vals.append(vals[-1])
        elif days[i] == days[i+1]:
            count += 1
            lim += 1
        elif days[i + 1] != start_date + timedelta(days=(i+1-count)):
            days.insert(i + 1,b)
            vals.insert(i + 1,vals[i])  
        i += 1
    
    if days[0] != days[1]:    
        days.insert(0,days[0])
        vals.insert(0,0)
    
def week_distance_sum_list(activities_df,date_string,activity):
    activities_df['Date'] = activities_df['Date'].apply(bf.convert_time)
    
    dists = activities_df['Distance'].tolist()
    dates = activities_df['Date'].tolist()
    types = activities_df['Activity Type'].tolist()
    
    #durs = []
    
    #for i in range(0,len(dur_strings)):
    #    dur = stringtime_to_floatminute(dur_strings[i])
    #    
    #    durs.append(dur)
    
    end_date = datetime.strptime(date_string,'%Y-%m-%d')
    #end_date = datetime.timestamp(date_strf)
    sta_date = end_date - timedelta(days=6)
    #print(end_date)
    #print(sta_date)
    
    #temp_date = sta_date - timedelta(days=1)
    
    days = [sta_date]
    vals = [0]
    #days = []
    #vals = []
    
    for i in range(0,len(dates)):
        #date_obj = datetime.strptime(dates[i],'%Y-%m-%d %H:%M:%S')
        #date_str = datetime.strftime(date_obj,'%Y-%m-%d')
        date_str = datetime.strftime(dates[i],'%Y-%m-%d')
        date_obj = datetime.strptime(date_str,'%Y-%m-%d')
        
        if date_obj >= sta_date and date_obj <= end_date and activity in types[i]:
            if len(vals) > 0:
                dist_sum = vals[-1] + dists[i]
            else:
                dist_sum = dists[i]
            
            vals.append(dist_sum)
            
            day_string = datetime.strftime(date_obj,'%Y-%m-%d')
            day_strf = datetime.strptime(day_string,'%Y-%m-%d')
            
            days.append(day_strf)
    
    populate_list(sta_date,end_date,days,vals)
    
    #print(days)
    #print(vals)
    
    return(days, vals)
    
def plot_week_previous_distances(activities_df,date_string,activity):
    
    title = '{} activities in the two previous weeks'.format(activity)
    
    if activity == 'All':
        activity = 'i'
    
    curr_week = datetime.strptime(date_string,'%Y-%m-%d')
    prev_week = curr_week - timedelta(days=7)
    #print(prev_week)
    prev_string = datetime.strftime(prev_week,'%Y-%m-%d')
    
    curr_days,curr_vals = week_distance_sum_list(activities_df,date_string,activity)
    curr_days = order_date_vals(curr_days)
    curr_annot = 'This week: {}km'.format(round(curr_vals[-1],2))
    prev_days,prev_vals = week_distance_sum_list(activities_df,prev_string,activity)
    prev_days = order_date_vals(prev_days)
    prev_annot = 'Last week: {}km'.format(round(prev_vals[-1],2))
    
    fig,ax = plt.subplots()
    plt.plot(prev_days,prev_vals,color='blue',label=prev_annot)
    
    plt.plot(curr_days,curr_vals,color='red',label=curr_annot)
    
    x_labels = []
    i = 0
    while i < 7:
        day = datetime.strptime(date_string,'%Y-%m-%d') - timedelta(days=(7+i))
        tag = datetime.strftime(day,'%a')
        x_labels.append(tag)
        i += 1
    
    x_labels.reverse()
    #0.5,1.5,2.5,3.5,4.5,5.5,6.5
    ax.set_xticks([1,2,3,4,5,6,7])
    ax.set_xticklabels(x_labels)
    
    ax.set_ylabel('Distance (km)')
    
    ax.legend(); 
    plt.title(title)


"""
def add_times(a,b):
    #requires times in minutes, or at least same units

    time = a_mins + b_mins
    
    return(time)
"""
  
def split_rank(user_df,activity_number,distance,kind='all'):
    
    #split = dr.activity_splits(user_df,activity_number,distance)
    
    index = user_df.loc[user_df['Activity number'] == str(activity_number)].index.values[0]
    split = user_df.at[index,distance]
    
    if split != 'NONE':
    
        ac_type = dr.activity_details(user_df,activity_number,'Type')
        ac_date = dr.activity_details(user_df,activity_number,'Date')
    
        user_df = user_df.loc[user_df['Activity Type'] == ac_type]
    
        user_df = user_df.loc[user_df[distance] != 'NONE']
    
        if kind == 'then':
            user_df = user_df.loc[user_df['Date'] <= ac_date]
    
        user_df = user_df.sort_values(by=[distance,'Date'],ascending=True)
    
        user_df = user_df.loc[user_df[distance] <= split]
    
        #ac_nos = user_df['Activity number'].tolist()
        times = user_df[distance].tolist()
    
        ranks = [1]
        #stop = False
        
        for i in range(1,len(times)):
        
            if times[i] == times[i-1]:
                ranks.append(ranks[-1])
            else:
                ranks.append(i+1)
        
        n_splits = len(user_df.loc[user_df[distance] == split].index.values) 
        
        if n_splits > 1:
            j = '='
        else:
            j = ''
        
        rank = f'{j}{ranks[-1]}'
    
    else:
        rank = 'NONE'
    
    return(rank)

def greatest_rank(user_df,activity_number,dist_dur,kind='all'):
    
    if dist_dur == 'Duration':
        dist_dur = 'Time'
    
    ac_type = dr.activity_details(user_df,activity_number,'Type')
    ac_date = dr.activity_details(user_df,activity_number, 'Date')
    
    val = dr.activity_details(user_df,activity_number,dist_dur)
    
    user_df = user_df.loc[user_df['Activity Type'] == ac_type]
    
    if kind == 'then':
        user_df = user_df[user_df['Date'] <= ac_date]
    
    #if dist_dur == 'Time':
    #    user_df[dist_dur] = user_df[dist_dur].apply(bf.stringtime_to_floatminute)
    #    val = bf.stringtime_to_floatminute(val)
          
    #user_df = user_df.sort_values(by=[dist_dur],ascending=False)#don't know about date ordering - hopefully leaves...
        
    #print(user_df[dist_dur].head())
 
    #user_df = user_df.loc[user_df[dist_dur] < val]
    
    #print(user_df[dist_dur].head())
    
    #vals = user_df[dist_dur].tolist()
    
    #ranks = [1]
        #stop = False
        
    #for i in range(1,len(vals)):
        
    #    if vals[i] == vals[i-1]:
    #        ranks.append(ranks[-1])
    #    else:
    #        ranks.append(i+1)
    
    user_df = user_df[user_df[dist_dur]>=val]
    
    n_splits = len(user_df.loc[user_df[dist_dur] == val].index.values) 
    
    user_df[dist_dur] = user_df[dist_dur].apply(lambda x: str(x))
    user_df['count'] = 1
    #user_df = user_df[[dist_dur,'count']].groupby(dist_dur).sum().reset_index()
    ranking = len(user_df[dist_dur].unique())
        
    if n_splits > 1:
        j = '='
    else:
        j = ''
        
    rank = f'{j}{ranking}'
    
    return(rank)

def count(user_df,ac_no,dist_dur,kind='all'):
    
    if dist_dur == 'Duration':
        dist_dur = 'Time'
    
    ac_type = dr.activity_details(user_df,ac_no,'Type')
    
    user_df = user_df.loc[user_df['Activity Type'] == ac_type]
    
    if kind == 'then':
        date = dr.ac_detail(ac_no,'Date')
        user_df = user_df.loc[user_df['Date'] <= date]
        
    n = len(user_df)
    
    return(n)

def split_count(user_df,distance,ac_no='none'):
    
    user_df = user_df.loc[user_df[distance] != 'NONE']
    
    if ac_no != 'none':
        date = dr.ac_detail(ac_no,'Date')
        user_df = user_df.loc[user_df['Date'] <= date]
        
    n = len(user_df)
                
    return(n)

def fastest_since(user_df,activity_number,distance,html_option=False):
    
    split = dr.activity_splits(user_df,activity_number,distance)
    
    ac_numbers = user_df['Activity number'].tolist()
    dates = user_df['Date'].tolist()
    splits = user_df[distance].tolist()
    
    ac_numbers.reverse()
    dates.reverse()
    splits.reverse()
    
    user_df['dates_dt'] = user_df['Date'].apply(bf.convert_time)
    
    dates_dt = user_df['dates_dt'].tolist()
    dates_dt.reverse()
    
    date_dt = dr.ac_detail(activity_number,'Date')
    date_dt = bf.convert_time(date_dt)
    
    found = False
    cont = True
    slowest = True
    
    date = []
    number = []
    split_list = []
    
    while cont == True:
        for i in range(0,len(splits)):
            if splits[i] != 'NONE':
                if splits[i] > split and slowest == True:
                    slowest = False
                if splits[i] < split and dates_dt[i] < date_dt:
                    date.append(dates[i])
                    number.append(ac_numbers[i])
                    split_list.append(splits[i])
                    cont = False
                    found = True
            if i == len(splits) - 1:
                cont = False
    
    if found == False:
        if slowest == False:
            out = 'PB!'
        else:
            out = 'unPB!'
    elif split == 'NONE':
        out = 'not run'
    else:
        if html_option == False:
            out = f'fastest since {date[0][:10]}'
        else:
            out = f"fastest since <a href='../{number[0]}'>{date[0][:10]}</a>: {split_list[0][-8:]}"
    
    return(out)
        
def fastest_after(user_df,activity_number,distance,html_option=False):
    
    split = dr.activity_splits(user_df,activity_number,distance)
    
    rank = split_rank(user_df, activity_number, distance)
    
    date = dr.activity_details(user_df,activity_number,'Date')
    
    user_df = user_df.loc[user_df['Date'] > date]
    
    if rank == 1:
        out = 'PB!'
    elif len(user_df) == 0:
        out = 'not run since'
    else:        
        user_df = user_df.loc[user_df[distance] < split]
        
        if len(user_df) == 0:
            out = 'not beaten since'
                
        else:
            #out_no = user_df['Activity number'].tolist()[0]
            out_date = str(user_df['Date'].tolist()[0])[:10]
            split_time = str(user_df[distance].tolist()[0][-8:])
               
            if html_option == False:
                out = f'beaten on {out_date}'
            else:
                out_no = user_df['Activity number'].tolist()[0]
                out = f"beaten on <a href='../{out_no}'>{out_date}</a>: {split_time}"
    
    return(out)
    
def last_run(user_df,activity_number,distance):
    
    date = dr.activity_details(user_df,activity_number,'Date')
    
    user_df = user_df[user_df['Activity Type']=='Running']
    user_df = user_df[(user_df['Date']<date)&(user_df[distance]!='NONE')].reset_index()

    if len(user_df) > 0:
        date = str(user_df.iloc[-1]['Date'])[:10]
        split = str(user_df.iloc[-1][distance])[-8:]
    
        string = f'{date}: {split}'
    else:
        string = 'N/A'
    
    return(string)

def next_run(user_df,activity_number,distance):
    
    date = dr.activity_details(user_df,activity_number,'Date')
    
    user_df = user_df[user_df['Activity Type']=='Running']
    user_df = user_df[(user_df['Date']>date)&(user_df[distance]!='NONE')].reset_index()

    if len(user_df) > 0:
        date = str(user_df.iloc[0]['Date'])[:10]
        split = str(user_df.iloc[0][distance])[-8:]
    
        string = f'{date}: {split}'
    else:
        string = 'N/A'
    
    return(string)


#greatest_rank(ws_df,ac_no,'Distance')
#greatest_rank(ws_df,ac_no,'Time')


def greatest_since(user_df,activity_number,dist_dur):
    
    split = dr.activity_splits(user_df,activity_number,dist_dur)
    
    ac_type = dr.activity_details(user_df,activity_number,'Type')
    #print(ac_type)
    #ac_numbers = user_df['Activity number'].tolist()
    dates = user_df['Date'].tolist()
    splits = user_df[dist_dur].tolist()
    types = user_df['Activity Type'].tolist()
    
    dates.reverse()
    splits.reverse()
    types.reverse()
    
    #print(type(dates[0]))
    
    #user_df['date_dt'] = user_df['Date'].apply(lambda x : datetime.strptime(x, '%Y'))
    
    found = False
    cont = True
    
    date = []
    split_list =[]
    
    for i in range(0,len(splits)):
        #print(ac_type,types[i],splits[i],split,cont)
        if ac_type == types[i] and splits[i] > split and cont == True:
            date.append(dates[i])
            split_list.append(splits[i])
            cont = False
            found = True
    
    if found == False:
        if 'Time' in dist_dur:
            out = 'longest!'
        if 'Dist' in dist_dur:
            out = 'furthest!'
    else:
        if 'Time' in dist_dur:
            out = f'longest since {date[0][:10]}: {split_list[0][-8:]}'
        if 'Dist' in dist_dur:
            out = f'furthest since {date[0][:10]} {split_list[0][-8:]}'
    
    return(out)

def greatest_since_two(user_df,activity_number,dist_dur):
    
    if dist_dur == 'Duration':
        dist_dur = 'Time'
        
    user_df['Date'] = user_df['Date'].apply(bf.convert_time)
    
    SPLIT = dr.activity_splits(user_df,activity_number,dist_dur)
    DATE = dr.activity_splits(user_df,activity_number,'Date')
    DATE = bf.convert_time(DATE)
    ac_type = dr.activity_details(user_df,activity_number,'Type')
    
    df = user_df[user_df['Activity Type'] == ac_type]
    df = df[df['Date'] < DATE]
    
    full_length = len(df)
    
    df = df[df[dist_dur] >= SPLIT]
    
    df = df.sort_values(by=['Date'],ascending=True).reset_index()
    
    if len(df) == 0:
        if 'Time' in dist_dur:
            out = 'longest ever!'
        if 'Dist' in dist_dur:
            out = 'further ever!'
    elif len(df) == full_length:
        out = 'shortest ever!'
    else:
        date = df.iloc[-1]['Date']
        ac_no = df.iloc[-1]['Activity number']
        if 'Time' in dist_dur:
            out = f"longest since <a href='../{ac_no}'>{str(date)[:10]}</a>"
        if 'Dist' in dist_dur:
            out = f"furthest since <a href='../{ac_no}'>{str(date)[:10]}</a>"

    return(out)

def greatest_until(user_df,activity_number,dist_dur):
    
    if dist_dur == 'Duration':
        dist_dur = 'Time'
        
    user_df['Date'] = user_df['Date'].apply(bf.convert_time)
    
    
    SPLIT = dr.activity_splits(user_df,activity_number,dist_dur)
    DATE = dr.activity_splits(user_df,activity_number,'Date')
    DATE = bf.convert_time(DATE)
    ac_type = dr.activity_details(user_df,activity_number,'Type')
    
    df = user_df[user_df['Activity Type'] == ac_type]
    df = df[df['Date'] > DATE]
    
    if len(df) == 0:
        out = 'no run since'
    else:
        df = df[df[dist_dur] >= SPLIT]
        if len(df) == 0:
            out = 'not beaten since'
        else:
            df = df.sort_values(by=['Date'],ascending=True).reset_index()            
        
            date = df.iloc[0]['Date']
            ac_no = df.iloc[0]['Activity number']
            if 'Time' in dist_dur:
                out = f"longest until <a href='../{ac_no}'>{str(date)[:10]}</a>"
            if 'Dist' in dist_dur:
                out = f"furthest until <a href='../{ac_no}'>{str(date)[:10]}</a>"

    return(out)


#AB5G2247.FIT

#ws_df = dr.pull_data('WS')
#print('Pulled')
#print(fastest_since(ws_df,'AB5G2247','1.5 mile'))

def html_activity_line(distance, user_df, ac_number,html_option=False):
    
    if distance == 'Half':
        text = 'Half marathon'
    elif distance == 'Full':
        text = 'Marathon'
    else:
        text = distance
    
    line = f"<b>{text}</b>: {str(dr.activity_splits(user_df,ac_number,distance))[-8:]} - {dr.split_rank(user_df,ac_number,distance)}/{dr.split_count(user_df,distance)} - {fastest_since(user_df,ac_number,distance,html_option)}"
    
    return(line)

#ac_no = dr.latest_activity('WS')
#ws_df = dr.pull_data('WS')
#print(html_activity_line('1km',ws_df,ac_no))    


def html_activity_lines(user_df, ac_number,html_option=False):
    
    text = f"{html_activity_line('1km', user_df, ac_number,html_option)}"
    
    options = ['1 mile', '1.5 mile', '3 mile', '5km', '10km', '20km', 'Half', 'Full']
    
    for i in range(0,len(options)):
        
        sec = f"""<br>
{html_activity_line(options[i], user_df, ac_number,html_option)}"""
    
        if 'NONE' not in sec:
            text = text + sec
         
    text = text + f"""<br>
<b>Distance</b>: {dr.activity_details(user_df,ac_number,'Distance')}km - {greatest_rank(user_df,ac_number,'Distance')} - {greatest_since(user_df,ac_number,'Distance')}<br>
<b>Duration</b>: {dr.activity_details(user_df,ac_number,'Time')} - {greatest_rank(user_df,ac_number,'Time')} - {greatest_since(user_df,ac_number,'Time')}""" 
            
    full = f"""<p>
{text}
</p>"""

    return(full)

def cropped_activity_lines(user_df,ac_number):
    
    html = html_activity_lines(user_df,ac_number,html_option=True)[3:-4]
    
    return(html)
    
def pace_as_string(user_df,ac_no,distance_tag):
    
    distance = distance_tag
    
    try:
        user_df = user_df.loc[user_df[distance] != 'NONE']
        
        index = user_df.loc[user_df['Activity number'] == str(ac_no)].index.values[0]
        split = user_df.at[index,distance]
        split = bf.split_to_floatminute(split)
        dist = dr.dist_dict[distance]/1000
        pace = split/dist
        pace = bf.floatminute_to_stringtime(pace)
    except:
        pace= 'NONE'
    
    if distance == 'Distance':
        t = dr.activity_details(user_df,ac_no,'Time')
        t = bf.split_to_floatminute(t)
        d = dr.activity_details(user_df,ac_no,'Distance')
        p = t/d
        pace = bf.floatminute_to_stringtime(p)
    
    return(pace)

def speed_as_string(user_df,ac_number):
    
    t = dr.activity_details(user_df,ac_number,'Time')
    t = bf.split_to_floatminute(t)
    d = dr.activity_details(user_df,ac_number,'Distance')
    speed = round(d/t * 60,1)
    speed = str(speed)+'km/h'
    return(speed)
    


def html_activity_row(distance, user_df, ac_number,html_option=False):
    
    if distance == 'Half':
        text = 'Half marathon'
    elif distance == 'Full':
        text = 'Marathon'
    else:
        text = distance
    
    durl = bf.dtag_to_durl(distance)
    
    line = f"""<tr>
<td>{text}</td>
<td><a href='map/{durl}'>{str(dr.activity_splits(user_df,ac_number,distance))[-8:]}</a></td>
<td>{pace_as_string(user_df,ac_number,distance)}</td>
<td>{split_rank(user_df,ac_number,distance,kind='then')}</td>
<td>{split_count(user_df,distance,ac_no=ac_number)}</td>
<td>{split_rank(user_df,ac_number,distance,kind='all')}</td>
<td>{split_count(user_df,distance)}</td>  
<td>{fastest_since(user_df,ac_number,distance,html_option)}</td>
<td>{last_run(user_df,ac_number,distance)}</td>
<td>{fastest_after(user_df,ac_number,distance,html_option)}</td>  
<td>{next_run(user_df,ac_number,distance)}</td>
</tr>"""

    #f"<b>{text}</b>: {str(dr.activity_splits(user_df,ac_number,distance))[-8:]} - {dr.split_rank(user_df,ac_number,distance)}/{dr.split_count(user_df,distance)} - {fastest_since(user_df,ac_number,distance,html_option)}"
    
    return(line)

#ac_no = dr.latest_activity('WS')
#ws_df = dr.pull_data('WS')
#print(html_activity_line('1km',ws_df,ac_no))    


def html_activity_rows(user_df, ac_number,html_option=False):
    
    text = ''
    #f"{html_activity_row('1km', user_df, ac_number,html_option)}"
    
    if 'NONE' in text:
        text = ''
    
    options = list(dr.dist_dict.keys())
    #['1 mile', '1.5 mile', '3 mile', '5km', '10km', '20km', 'Half', 'Full']
    
    for i in range(0,len(options)):
        
        sec = f"""{html_activity_row(options[i], user_df, ac_number,html_option)}"""
    
        if 'NONE' not in sec:
            text = text + sec
            
    text = text + f'''<tr>
<td>Distance</td>
<td>{dr.activity_details(user_df,ac_number,'Distance')}km</td>
<td>{pace_as_string(user_df, ac_number, 'Distance')}</td>
<td>{greatest_rank(user_df,ac_number,'Distance',kind='then')}</td>
<td>{count(user_df,ac_number,'Distance',kind='then')}</td>
<td>{greatest_rank(user_df,ac_number,'Distance',kind='all')}</td>
<td>{count(user_df,ac_number,'Distance',kind='all')}</td>  
<td>{greatest_since_two(user_df,ac_number,'Distance')}</td>   
<td>{last_run(user_df,ac_number,'Distance')}km</td>
<td>{greatest_until(user_df,ac_number,'Distance')}</td> 
<td>{next_run(user_df,ac_number,'Distance')}km</td>
</tr>

<tr>
<td>Duration</td>
<td>{dr.activity_details(user_df,ac_number,'Time')}</td>
<td>{speed_as_string(user_df,ac_number)}</td>
<td>{greatest_rank(user_df,ac_number,'Duration',kind='then')}</td>
<td>{count(user_df,ac_number,'Duration',kind='then')}</td>
<td>{greatest_rank(user_df,ac_number,'Duration',kind='all')}</td>
<td>{count(user_df,ac_number,'Duration',kind='all')}</td>  
<td>{greatest_since_two(user_df,ac_number,'Time')}</td>  
<td>{last_run(user_df,ac_number,'Time')}</td>
<td>{greatest_until(user_df,ac_number,'Time')}</td>   
<td>{next_run(user_df,ac_number,'Time')}</td>
</tr>
'''
    
    #f"""<br>
#<b>Distance</b>: {dr.activity_details(user_df,ac_number,'Distance')}km - {greatest_rank(user_df,ac_number,'Distance')} - {greatest_since(user_df,ac_number,'Distance')}<br>
#<b>Duration</b>: {dr.activity_details(user_df,ac_number,'Time')} - {greatest_rank(user_df,ac_number,'Time')} - {greatest_since(user_df,ac_number,'Time')}""" 
            
    #full = f"""{text}"""

    return(text)

def cropped_activity_table(user_df,ac_number):
    
    #html = html_activity_lines(user_df,ac_number,html_option=True)[3:-4]
    
    html = f'''
    
<th>Distance</th>
<th>Time</th>
<th>Pace</th>
<th colspan="2">Then</th>
<th colspan="2">Now</th>
<th colspan='2' style='text-align: centre;'>Before</th>
<th colspan='2'>Since</th>
    
{html_activity_rows(user_df,ac_number,html_option=True)}

'''
    
    return(html)

"""
<b>1km</b>: {dr.activity_splits(user_df,ac_number,'1km')}: {dr.split_rank(user_df,ac_number,'1km')}/{dr.split_count(user_df,'1km')} - {fastest_since(user_df,ac_number,'1km')}<br>
<b>1 mile</b>: {dr.activity_splits(user_df,ac_number,'1 mile')}: {dr.split_rank(user_df,ac_number,'1 mile')}/{dr.split_count(user_df,'1 mile')} - {fastest_since(user_df,ac_number,'1 mile')}<br>
<b>1.5 mile</b>: {dr.activity_splits(user_df,ac_number,'1.5 mile')}: {dr.split_rank(user_df,ac_number,'1.5 mile')}/{dr.split_count(user_df,'1.5 mile')} - {fastest_since(user_df,ac_number,'1.5 mile')}<br>
<b>3 mile</b>: {dr.activity_splits(user_df,ac_number,'3 mile')}: {dr.split_rank(user_df,ac_number,'3 mile')}/{dr.split_count(user_df,'3 mile')} - {fastest_since(user_df,ac_number,'3 mile')}<br>
<b>5km</b>: {dr.activity_splits(user_df,ac_number,'5km')}: {dr.split_rank(user_df,ac_number,'5km')}/{dr.split_count(user_df,'5km')} - {fastest_since(user_df,ac_number,'5km')}<br>
<b>10km</b>: {dr.activity_splits(user_df,ac_number,'10km')}: {dr.split_rank(user_df,ac_number,'10km')}/{dr.split_count(user_df,'10km')} - {fastest_since(user_df,ac_number,'10km')}<br>
<b>20km</b>: {dr.activity_splits(user_df,ac_number,'20km')}: {dr.split_rank(user_df,ac_number,'20km')}/{dr.split_count(user_df,'20km')} - {fastest_since(user_df,ac_number,'20km')}<br>
<b>Half marathon</b>: {dr.activity_splits(user_df,ac_number,'Half')}: {dr.split_rank(user_df,ac_number,'Half')}/{dr.split_count(user_df,'Half')} - {fastest_since(user_df,ac_number,'Half')}<br>
<b>Full</b>: {dr.activity_splits(user_df,ac_number,'Full')}: {dr.split_rank(user_df,ac_number,'Full')}/{dr.split_count(user_df,'Full')} - {fastest_since(user_df,ac_number,'Full')}</p></body>
"""

#df = dr.pull_data('WS')    
#print(html_activity_lines(ws_df,ac_no)) 
    
#df = dr.pull_data('WS')    
#print(html_assessment(df,'AABB0534'))

#print(html_assessment('A85I1222'))
    

    
#print(simple_week_update_html(today_string))
            
def plot_distances_equiv_month(user_df,m,yyyy,activity):
    types = user_df['Activity Type'].tolist()
    dates = user_df['Date'].tolist()
    
    run_vals = []    
    
    title = '{} distances in {}'.format(activity,bf.month_caller(m))
    
    if activity == 'All':
        activity = 'i'
    
    for i in range(0,len(dates)):
        if activity in types[i] and f'-{bf.add_zeros(m)}-' in str(dates[i]):
            run_vals.append(i)
    val = run_vals[0]
    earliest_date = str(dates[val])
    earliest_year = int(earliest_date[:4])
    
    #pick_month = yyyy * 12 + m
    #earl_month = datestring_to_floatmonth(earliest_date)
    
    fig,ax = plt.subplots()
    for y in range(earliest_year,yyyy+1):
        temp_dates,temp_sum = month_dist_sum(m,y,activity)
        temp_label = f'{y}: {temp_sum[-1]}km'
        plt.plot(temp_dates,temp_sum,label=temp_label)
    
    if yyyy+1 - 2016 > 6:    
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        ax.legend();
    
    plt.title(title)

#df = dr.pull_data('WS')    
#time_check()
#plot_distances_equiv_month(df,2,2021,'Running')
#time_check()
    
def activity_comparisons_ex(user_df,activity_number):
    ac_type = dr.activity_details(user_df,activity_number,'Type')
    dist = dr.activity_details(user_df,activity_number,'Distance')
    dur = dr.activity_details(user_df,activity_number,'Duration')
    dur = bf.stringtime_to_floatminute(dur)
    
    ac_nos = user_df['Activity number'].tolist()
    ac_types = user_df['Activity Type'].tolist()
    dists = user_df['Distance'].tolist()
    durs = user_df['Time'].tolist()
    
    for i in range(0,len(ac_nos)):
        if ac_types[i] == ac_type and ac_nos[i] != activity_number and dists[i]<25:
            i_dur = bf.tringtime_to_floatminute(durs[i])
            plt.scatter(dists[i],i_dur,s=15,color='blue')
            
    plt.scatter(dist,dur,color='red')
    
    plt.xlabel("Distance (km)")
    plt.ylabel('Duration (mins)')
    
def activity_comparisons(user_df,activity_number):
    ac_type = dr.activity_details(user_df,activity_number,'Type')
    dist = dr.activity_details(user_df,activity_number,'Distance')
    dur = dr.activity_details(user_df,activity_number,'Duration')
    dur = bf.stringtime_to_floatminute(dur)
    
    #plot_df = user_df.loc(user_df['Activity Type'] == ac_type)
    plot_df = user_df[user_df['Activity Type'].isin([ac_type])]
    plot_df = plot_df.loc[plot_df['Distance'] < 25]
    plot_df = plot_df.loc[plot_df['Activity number'] != activity_number]
    plot_df['Time'] = plot_df['Time'].apply(bf.stringtime_to_floatminute)
     
    plt.scatter(plot_df['Distance'],plot_df['Time'],s=15,color = 'blue')
       
    plt.scatter(dist,dur,color='red')
    
    plt.xlabel("Distance (km)")
    plt.ylabel('Duration (mins)')
    
def activity_comparisons_plotly(user_df,activity_number):
    
    #bf.time_check()
    
    ac_type = dr.activity_details(user_df,activity_number,'Type')
    dist = dr.activity_details(user_df,activity_number,'Distance')
    dur = dr.activity_details(user_df,activity_number,'Duration')
    date = dr.activity_details(user_df,activity_number,'Date')
    #dur = bf.stringtime_to_floatminute(dur)
    
    #plot_df = user_df.loc(user_df['Activity Type'] == ac_type)
    plot_df = user_df[user_df['Activity Type'].isin([ac_type])]
    if dist < 25:
        plot_df = plot_df.loc[plot_df['Distance'] < 25]
    else:
        plot_df = plot_df.loc[plot_df['Distance'] < dist+3]
    
    plot_df['Time'] = plot_df['Time'].apply(bf.stringtime_to_floatminute)
    
    base_df = plot_df.loc[plot_df['Activity number'] != activity_number]
    
    base_dates = base_df['Date'].tolist()
    bac_ac = base_df['Activity number'].tolist()
    
    ac_df = plot_df.loc[plot_df['Activity number'] == activity_number]
    
    ac_dates = ac_df['Date'].tolist()
    
    #bf.time_check()
    
    hover_t = '''%{text}<br>
%{x}, %{y}<extra></extra>'''

    hover_t = '''%{text}<br><extra></extra>'''
    
    t_base = ["<a href='/index/{}' style='color:white;'>{}</a>".format(bac_ac[i],base_dates[i]) for i in range(len(base_df))]
    t_ac = ['{}'.format(ac_dates[i]) for i in range(len(ac_dates))]
    
    fig = go.Figure()
    
    fig.add_trace(
    go.Scatter(
        mode='markers',
        x=base_df['Distance'],
        y=base_df['Time'],
        #text = base_df['Date'],
        marker=dict(
            color='Green'
            ),
        hovertemplate = hover_t,
        text = t_base,
        showlegend = False,
        
        )
    )
    
    fig.add_trace(
    go.Scatter(
        mode='markers',
        x=ac_df['Distance'],
        y=ac_df['Time'],
        #text = ac_df['Date'],
        marker=dict(
            color='Red'
            ),
        hovertemplate = hover_t,
        text = t_ac,
        showlegend = False
        )
    )

    fig.update_layout(
        xaxis_title='Distance (km)',
        yaxis_title='Time (m)')
    
    #fig = px.scatter(base_df,x='Distance',y='Time',hover_data=['Date'])
    
    #print('3?')
    #bf.time_check()
    
    #fig.update_traces({'name':'1st dose','showlegend': False})
    
    #bf.time_check()
    
    #fig.add_scatter(x=ac_df['Distance'],y=ac_df['Time'],customdata=ac_df['Date'], showlegend = False,
                    #hovertemplate = 'Date=%{customdata}')
    
    #bf.time_check()
    
    div = pio.to_html(fig,auto_play=False,full_html=False)
    
    #bf.time_check()
    
    return(div)
    

#print('start')
#time_check()    
#df = dr.pull_data('WS')
#time_check()
#activity_comparisons_ex(df,'B2AE1701')
#time_check()
#activity_comparisons(df,'B2AE1701')
#time_check()
#print('done')
    
def shoes_distance(user_df,pair_of_shoes,ac_no='NONE'):
    
    df = user_df.loc[user_df['Shoes'] == pair_of_shoes]
    
    if ac_no != 'NONE':
        date = dr.activity_details(df,ac_no,'Date')
        df['Date'] = df['Date'].apply(bf.convert_time)
        date = bf.convert_time(date)
        df = df.loc[df['Date'] <= date]
    
    shoe_distance = df['Distance'].sum()
    
    #shoes = user_df['Shoes'].tolist()  
    #dists = user_df['Distance'].tolist()    
    
    #shoe_dists = []
    
    #for i in range(0,len(shoes)):
    #    if pair_of_shoes == shoes[i]:
    #        shoe_dists.append(dists[i])
            
    #shoe_distance = round(sum(shoe_dists),1)
    
    return(shoe_distance)
    
def shoes_activity_line(user_df,activity_number):
    
    shoes = dr.activity_details(user_df,activity_number,'Shoes')
    
    if shoes != 'NONE':
        dist = round(shoes_distance(user_df,shoes,activity_number),2)
    
        ac_type = dr.activity_details(user_df,activity_number,'Activity Type')
    
        if ac_type == 'Running':
            factor = 1
        else:
            factor = 1.5
    
        if dist > 1000*factor:
            dist_html = f'<b><u>{dist}!!!</u></b>'
        elif dist > 800*factor:
            dist_html = f'<b><u>{dist}!</u></b>'
        elif dist > 600*factor:
            dist_html = f'<b><u>{dist}</u></b>'
        elif dist > 400*factor:
            dist_html = f'<u>{dist}</u>'
        else:
            dist_html = f'{dist}'
    
        html = f"""{shoes}: {dist_html}km"""
    else:
        html = ''
    
    return(html)
    
def shoe_rows(user_df):
        
    user_df['Date'] = user_df['Date'].apply(bf.convert_time)
    user_df = user_df.sort_values(by='Date',ascending=False)
    
    shoe_l_df = user_df.drop_duplicates('Shoes')
    shoe_l_df = shoe_l_df.loc[shoe_l_df['Shoes'] != 'NONE']
    shoe_l_df = shoe_l_df[shoe_l_df['Shoes']==shoe_l_df['Shoes']]
    shoes_list = shoe_l_df['Shoes'].tolist()
    
    rows = '''<th>Shoes</th>
    <th>Main</th>
    <th>First used</th>
    <th>Last used</th>
    <th>Total distance</th>'''
    
    for i in range(0,len(shoes_list)):
        shoes = shoes_list[i]
        #dist = round(shoes_total_dist(user_df, shoes),2)
        
        shoe_df = user_df.loc[user_df['Shoes'] == shoes]
        
        dist = round(shoe_df['Distance'].sum(),1)
        
        dates_l = shoe_df['Date'].tolist() 
        first = dates_l[-1]
        last = dates_l[0]
        links = shoe_df['Activity number'].tolist()
        f_link = f"<a href='/index/{links[-1]}'>"
        l_link = f"<a href='/index/{links[0]}'>"
        
        s_type = shoe_df['Activity Type'].value_counts().idxmax()
        
        row = f"""<tr>
<td>{shoes}</td>
<td>{s_type}</td>
<td>{f_link}{first}</a></td>
<td>{l_link}{last}</a></td>
<td>{dist}km</td>
</tr>        
"""
    
        rows = rows + row
        
    return(rows)
    
def shoes_plotly(user_df):
    
    user_df['Date'] = user_df['Date'].apply(bf.convert_time)
    user_df = user_df.sort_values(by='Date',ascending=True)
    
    shoe_l_df = user_df.drop_duplicates('Shoes')
    shoe_l_df = shoe_l_df.loc[-shoe_l_df['Shoes'].fillna('NONE').isin(['NONE','default',None])]
    shoes_list = shoe_l_df['Shoes'].tolist()
    
    fig = go.Figure()
    
    for i in range(0,len(shoes_list)):
        shoe = shoes_list[i]
        
        shoe_df = user_df.loc[user_df['Shoes'] == shoe]
        
        shoe_df['c_d'] = shoe_df['Distance'].cumsum()
        
        try:
            start_date = shoe_df['Date'].tolist()[0]
        except:
            raise ValueError(shoe, shoe_df)
        
        shoe_df = pd.concat([pd.DataFrame.from_dict({
            'Date': [start_date],
            'c_d': [0]
            }), shoe_df])
        
        #hover_t = '''<extra></extra>'''
        
        fig.add_trace(
            go.Scatter(
                mode='lines',
                name=shoe,
                x=shoe_df['Date'],
                y=shoe_df['c_d'],
                #hovertemplate = hover_t,
                hoverinfo = 'skip',
                showlegend = True
                ))
        
    
        
    div = pio.to_html(fig,auto_play=False,full_html=False)
    
    return(div)
    

def week_dist_sum(user_df,activity,start):
#    dists = user_df['Distance'].tolist()
#    dates = user_df['Date'].tolist()
#    activities = user_df['Activity Type'].tolist()
    
#    stamps = []##
    
#    for i in range(0,len(dates)):
#        stamp = datetime.strptime(dates[i],'%Y-%m-%d %H:%M:%S')
#        stamps.append(stamp)
    
#    fin = start + timedelta(days=7)
#    
#    dist = [0]
   
#    for i in range(0,len(dists)):
#        if activity in activities[i]:
#            if stamps[i] >= start and stamps[i] < fin:
#                dist.append(dist[-1] + dists[i])
                
#    final = dist[-1]
    
    ###
    
    fin = start + timedelta(days=7)
    #user_df['Date'] = user_df['Date'].apply(convert_time)
    #print(type('strt'))

#    plot_df = user_df.loc[user_df['Activity Type'] == activity]
    plot_df = user_df.loc[user_df['Date'] >= start]
    plot_df = plot_df.loc[plot_df['Date'] < fin]
    
    final = plot_df['Distance'].sum()
    
    return(final)
    
def prev_four_week_avg(user_df,activity,end):
    week_dists = []
    
    for i in range(0,4):
        start = end - timedelta(days=7*(i+1))
        dist = week_dist_sum(user_df,activity,start)
        week_dists.append(dist)
        
    avg = sum(week_dists)/4
    
    return(avg)

def plot_year_week_progress(user_df,activity,year):
    
    start_string = f'{year}-01-01'
    
    start = datetime.strptime(start_string,'%Y-%m-%d')
    
    xs = []
    dists = []
    avgs = []
    
    for i in range(0,52):
        sta = start + timedelta(days=7*i)
        dist = week_dist_sum(user_df,activity,sta)
        dists.append(dist)
        xs.append(i+0.5)
        
        end = start + timedelta(days=7*(i+1))
        avg = prev_four_week_avg(user_df,activity,end)
        avgs.append(avg)
    
    fig,ax = plt.subplots()
    
    plt.bar(xs,dists)
    plt.plot(xs,avgs,color='red')
    
    plt.xlim([0,52])
    
    ax.set_ylabel('Distance (km)')
    
    plt.title(f'Weekly {activity} distances in {year}')
    
#plt.show()
#ws_df = dr.pull_data('WS')
#plot_year_week_progress(ws_df,'Running',2020)
#plt.show()
#plot_year_week_progress(ws_df,'Running',2019)
#plt.show()
#plot_year_week_progress(ws_df,'Running',2018) 
#plt.show() 
#print(shoes_distance_html(ws_df,'4854330057'))

def plot_rolling_year_week_progress(user_df,activity,date_string):
    user_df['Date'] = user_df['Date'].apply(bf.convert_time)
    user_df = user_df.loc[user_df['Activity Type'] == activity]
    
    end = datetime.strptime(date_string,'%Y-%m-%d')
    end = end + timedelta(days=1)
    
    xs = []
    dists = []
    avgs = []
    
    ticks = []
    labels = []
    
    for i in range(0,52):
        sta = end - timedelta(days=7*(i+1))
        #print(sta)
        dist = week_dist_sum(user_df,activity,sta)
        dists.append(dist)
        xs.append(51.5 - i)
        
        fin = end - timedelta(days=7*(i))
        avg = prev_four_week_avg(user_df,activity,fin)
        avgs.append(avg)
        
        week_end = end - timedelta(days=7*(i))
        week_end_day = round(float(datetime.strftime(week_end,'%d')))
        
        if week_end_day <= 7:
            point = (51.5 - i) - 0.8 * (week_end_day - 4)/7
            month_sta = datetime.strftime(week_end,'%b')
            
            ticks.append(point)
            labels.append(month_sta)
            
    
    fig,ax = plt.subplots()
    
    plt.bar(xs,dists)
    plt.plot(xs,avgs,color='red')
    
    plt.xlim([0,52])
    
    ax.set_ylabel('Distance (km)')
    
    plt.xticks(ticks,labels)
    
    plt.title(f'Weekly {activity} distances till {date_string}')

#ws_df = dr.pull_data('WS')
#plot_rolling_year_week_progress(ws_df,'Walking',today_string)

#activity_comparisons(ws_df,'ABGG2939')
#plot_distances_equiv_month(ws_df,10,2020,'All')

def plot_rolling_year_week_day_progress(user_df,activity,date_string):
    
    end = datetime.strptime(date_string,'%Y-%m-%d')
    
    sta = end - timedelta(days=7*52)
    #print(sta)
    
    bar_xs = []
    dists = []
    line_xs = []
    avgs = []
    
    
    for i in range(0,52):
        week_sta = sta + timedelta(days=7*(i))
        dist = week_dist_sum(user_df,activity,week_sta)
        dists.append(dist)
        bar_xs.append(0.5+i)
        
        for n in range(0,7):
            month_fin = week_sta + timedelta(days=n)
            avg = prev_four_week_avg(user_df,activity,month_fin)
            avgs.append(avg)
            point = i + (n/7)
            line_xs.append(point)
    
    fig,ax = plt.subplots()
    
    plt.bar(bar_xs,dists,width=1)
    plt.plot(line_xs,avgs,color='red')
    
    plt.xlim([0,52])
    
    ax.set_ylabel('Distance (km)')
    
    plt.title(f'Weekly {activity} distances till {date_string}')
    
   #ws_df = dr.pull_data('WS')
#plot_rolling_year_week_day_progress(ws_df,'Running','2020-12-24')
#plt.show()
#time_check()
#plot_rolling_year_week_progress(ws_df,'Running','2021-02-10')
#time_check()

def otd_list(date,user_df):
    
    dates = user_df['Date'].tolist()
    activities = user_df['Activity number'].tolist()
    
    acs = []
    
    for i in range(0,len(dates)):
        if str(date)[5:11] in str(dates[i]) and date[:11] not in str(dates[i]):
           acs.append(activities[i])
           
    return(acs)       

#ws_df = dr.pull_data('WS')

#print(otd_list('2021-12-02',ws_df))


"""
def otd_html_site(date,user_df,img = 'N'):
    
    otd_acs = otd_list(date,user_df)
    
    lines = ''
    
    for i in range(0,len(otd_acs)):
        ac_no = otd_acs[i]
        ac_date = dr.activity_details(user_df,ac_no,'Date')
        ac_type = dr.activity_details(user_df,ac_no,'Type')
        ac_dist = dr.activity_details(user_df,ac_no,'Distance')
        ac_dur = dr.activity_details(user_df,ac_no,'Duration')
        
        line = f"{ac_date[:4]}: <a href='index/{ac_no}'>{ac_type}</a>, {ac_dist}km in {ac_dur}"
        
        if len(lines) == 0:
            lines = line
        else:
            lines = lines + f'''<br>
{line}'''

        if img != 'N' and ac_type != 'Cardio':
            try:
                ac_df = analyse.route_data(ac_no)
                tmb_test(ac_df,plot_size='small')#isn't actually small
            
                plt.savefig('temp_image.jpg')
    
                encoded = base64.b64encode(open('temp_image.jpg','rb').read()).decode()
    
                html_img = f"""
#<br>
#<img src='data:image/jpg;base64,{encoded}'>
"""
                #print(html_img)
                lines = lines + html_img
                
                os.remove('temp_image.jpg')
    
                #plt.show()
            
                #lines = lines + html_img
            except:
                print('broken data',ac_no,ac_date)
                   
            
    html = f'''
<u><b>On this day</b></u><br>
{lines}'''

    return(html)

"""

def otd_html_folium(date,user_df,img = 'N',index_link = True):
    
    otd_acs = otd_list(date,user_df)
    
    lines = ''
    
    for i in range(0,len(otd_acs)):
        if i == 0:
            intro = '<u><b>On this day</b></u><br>'
            lines = lines + intro
        
        ac_no = otd_acs[i]
        ac_date = dr.activity_details(user_df,ac_no,'Date')
        ac_type = dr.activity_details(user_df,ac_no,'Type')
        ac_dist = dr.activity_details(user_df,ac_no,'Distance')
        ac_dur = dr.activity_details(user_df,ac_no,'Duration')
        ac_rankings = dr.activity_details(user_df,ac_no,'Run Rankings')
        
        if index_link == True:
            link = f'index/{ac_no}'
        else:
            link = f'../{ac_no}'
        
        line = f"{ac_date[:4]}: <a href='{link}'>{ac_type}</a>, {ac_dist}km in {ac_dur} {interpret_rankings(ac_rankings)}"
        
        if i == 0:
            lines = lines + line
        else:
            lines = lines + f'''<br>
{line}'''

        if img != 'N' and ac_type != 'Cardio':
            #try:
            ac_df = dr.route_data(ac_no)
            if len(ac_df) == 0:
                raise ValueError(f'{ac_no} has no df: ',ac_df)
                
            html_js = osm_map(ac_df,30,30)
                
            lines = lines + html_js
                
                #os.remove('temp_image.jpg')
    
                #plt.show()
            
                #lines = lines + html_img
            #except:
            #print('broken data',ac_no,ac_date)
                   
            
    html = f'''
{lines}'''

    return(html)

#print(otd_html('2020-12-02',ws_df,img='Y'))

def reorder_polar_labels(unordered_ticks,unordered_labels):
    new_ticks = []
    new_labels = []
    
    for i in range(0,len(unordered_ticks)):
        if unordered_ticks[i] > 2 * pi:
            tick = unordered_ticks[i] - 2 * pi
        else:
            tick = unordered_ticks[i]
            
        if len(new_ticks) == 0:
            new_ticks.append(tick)
            new_labels.append(unordered_labels[i])
        elif tick > new_ticks[-1]:
            new_ticks.append(tick)
            new_labels.append(unordered_labels[i])
        elif tick < new_ticks[0]:
            new_ticks.insert(0,tick)
            new_labels.insert(0,unordered_labels[i])
        else:
            insert = False
            n = 1
            
            while insert == False:
                
                if tick < new_ticks[n]:
                    new_ticks.insert(n,tick)
                    new_labels.insert(n,unordered_labels[i])
                    insert = True
                
                n += 1
                
    return(new_ticks,new_labels)
            

def activities_in_week_for_wheel(user_df,activity_type,start_date):
    dates = user_df['Date'].tolist()
    types = user_df['Activity Type'].tolist()
    
    
    week = []
    
    for n in range(0,7):
        day = start_date + timedelta(days=n)
        day_string = datetime.strftime(day,'%Y-%m-%d')
        
        for i in range(0,len(dates)):
            if day_string in dates[i] and activity_type in types[i]:
                week.append(0.3+(n+1)/7)
                
    return(week)
            
def year_activity_wheel(user_df,activity,date_string,labels_on='N'):
    
    end = datetime.strptime(date_string,'%Y-%m-%d')
    
    sta = end - timedelta(days=7*52)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    
    x_ticks = []
    x_labels = []
    
    for i in range(0,52):
        week_sta = sta + timedelta(days=7*i)
        week = activities_in_week_for_wheel(user_df, activity, week_sta)
        
        if labels_on != 'N':
            val = - pi/2
        else:
            val = 0
        
        angle = 2 * pi * (i/52) + pi/2 + val
        angles = []
        
        for n in range(0,len(week)):
            angles.append(angle)
        
        if len(week) > 0:
            ax.scatter(angles, week,s=15)
            
        if i%8 == 0 and labels_on != 'N':
            date_label = f'''w/c
{str(week_sta)[:10]}'''
            x_ticks.append(angle)
            x_labels.append(date_label)
    
    #ax.set_yticks([1/7,2/7,3/7,4/7,5/7,6/7,1])        
    
    #plt.xticks(x_ticks,labels)
    
    #ax.set_xticks(x_ticks)
    #ax.set_xticklabels(labels)
    if labels_on != 'N':
        plt.yticks([1/7,2/7,3/7,4/7,5/7,6/7,1],'')
        plt.xticks(x_ticks,x_labels)
    
        ax.set_thetamin(0)
        ax.set_thetamax(360)
    else:
        plt.axis('off')
    
    title_date = datetime.strftime(sta,'%Y-%m-%d')
    
    plt.title(f'{activity}, {title_date} to {date_string}')
    
def activities_in_week_null(user_df,activity_type,start_date):
    dates = user_df['Date'].tolist()
    types = user_df['Activity Type'].tolist()
    
    week = []
    null = []
    
    for n in range(0,7):
        day = start_date + timedelta(days=n)
        day_string = datetime.strftime(day,'%Y-%m-%d')
        
        found = False
        
        for i in range(0,len(dates)):
            
            if day_string in dates[i] and activity_type in types[i]:
                week.append(0.5+(n+1)/7)
                found = True
                
        if found == False:
            null.append(0.5+(n+1)/7)
                
    return(week, null)
    
def year_activity_wheel_null(user_df,activity,date_string,labels_on='N'):
    
    end = datetime.strptime(date_string,'%Y-%m-%d')
    end = end + timedelta(days=1)
    
    sta = end - timedelta(days=7*52)
    
    title_date = datetime.strftime(sta,'%Y-%m-%d')
    
    title = f'{activity}, {title_date} to {date_string}'
    
    if activity == 'All':
        activity = 'i'
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    
    x_ticks = []
    x_labels = []
    
    for i in range(0,52):
        week_sta = sta + timedelta(days=7*i)
        week,null = activities_in_week_null(user_df, activity, week_sta)
        
        if labels_on != 'N':
            val = - pi/2
        else:
            val = 0
        
        angle = 2 * pi * (i/52) + pi/2 + val
        angles = []
        nangles = []
        
        for n in range(0,len(week)):
            angles.append(angle)
            
        for n in range(0,len(null)):
            nangles.append(angle)
        
        if len(week) > 0:
            ax.scatter(angles, week, s=15,color='red')
            
        if len(null) > 0:
            ax.scatter(nangles, null, s=5,color='black')
            
        if i%8 == 0 and labels_on != 'N':
            date_label = f'''w/c
{str(week_sta)[:10]}'''
            x_ticks.append(angle)
            x_labels.append(date_label)
    
    #ax.set_yticks([1/7,2/7,3/7,4/7,5/7,6/7,1])        
    
    #plt.xticks(x_ticks,labels)
    
    #ax.set_xticks(x_ticks)
    #ax.set_xticklabels(labels)
    if labels_on != 'N':
        plt.yticks([1/7,2/7,3/7,4/7,5/7,6/7,1],'')
        plt.xticks(x_ticks,x_labels)
    
        ax.set_thetamin(0)
        ax.set_thetamax(360)
    else:
        plt.axis('off')
    
    #title_date = datetime.strftime(sta,'%Y-%m-%d')
    
    plt.title(title)

#ws_df = dr.pull_data('WS')    
#year_activity_wheel_null(ws_df,'All','2021-01-06')
#plt.show()
#year_activity_wheel(ws_df,'Walking','2020-12-24')

def times_radar(user_df,activity_number):
    
    maxs = []
    mins = []
    
    qs = []#25th percentile - actually 33rd
    hs = []#50th percentile - actually 67th
    
    times = []
    
    dist = dr.activity_details(user_df,activity_number,'Distance') * 1000
    
    #print(dist)
    
    times.append(dr.activity_splits(user_df,activity_number,'1km'))
    times.append(dr.activity_splits(user_df,activity_number,'1 mile'))             
    times.append(dr.activity_splits(user_df,activity_number,'1.5 mile'))
    
    maxs.append(dr.split_percentile(user_df,'1km',0.95))
    qs.append(dr.split_percentile(user_df,'1km',0.33))
    hs.append(dr.split_percentile(user_df,'1km',0.67))
    mins.append(dr.split_extremes(user_df,'1km','min'))
    maxs.append(dr.split_percentile(user_df,'1 mile',0.95))
    qs.append(dr.split_percentile(user_df,'1 mile',0.33))
    hs.append(dr.split_percentile(user_df,'1 mile',0.67))
    mins.append(dr.split_extremes(user_df,'1 mile','min'))
    maxs.append(dr.split_percentile(user_df,'1.5 mile',0.95))
    qs.append(dr.split_percentile(user_df,'1.5 mile',0.33))
    hs.append(dr.split_percentile(user_df,'1.5 mile',0.67))
    mins.append(dr.split_extremes(user_df,'1.5 mile','min'))
    
    if dist >= 4828.03:
        times.append(dr.activity_splits(user_df,activity_number,'3 mile'))
        qs.append(dr.split_percentile(user_df,'3 mile',0.33))
        hs.append(dr.split_percentile(user_df,'3 mile',0.67))
        maxs.append(dr.split_percentile(user_df,'3 mile',0.95))
        mins.append(dr.split_extremes(user_df,'3 mile','min'))
    
    if dist >= 5000:
        times.append(dr.activity_splits(user_df,activity_number,'5km'))
        qs.append(dr.split_percentile(user_df,'5km',0.33))
        hs.append(dr.split_percentile(user_df,'5km',0.67))
        maxs.append(dr.split_percentile(user_df,'5km',0.95))
        mins.append(dr.split_extremes(user_df,'5km','min'))
        
    if dist >= 10000:
        times.append(dr.activity_splits(user_df,activity_number,'10km'))
        qs.append(dr.split_percentile(user_df,'10km',0.33))
        hs.append(dr.split_percentile(user_df,'10km',0.67))
        maxs.append(dr.split_percentile(user_df,'10km',0.95))
        mins.append(dr.split_extremes(user_df,'10km','min'))
        
    if dist >= 20000:
        times.append(dr.activity_splits(user_df,activity_number,'20km'))
        qs.append(dr.split_percentile(user_df,'20km',0.33))
        hs.append(dr.split_percentile(user_df,'20km',0.67))
        maxs.append(dr.split_percentile(user_df,'20km',0.95))
        mins.append(dr.split_extremes(user_df,'20km','min'))
        
    if dist >= 21097.7:
        times.append(dr.activity_splits(user_df,activity_number,'Half'))
        qs.append(dr.split_percentile(user_df,'Half',0.33))
        hs.append(dr.split_percentile(user_df,'Half',0.67))
        maxs.append(dr.split_percentile(user_df,'Half',0.95))
        mins.append(dr.split_extremes(user_df,'Half','min'))

    if dist >= 42195:
        times.append(dr.activity_splits(user_df,activity_number,'Full'))
        qs.append(dr.split_percentile(user_df,'Full',0.33))
        hs.append(dr.split_percentile(user_df,'Full',0.67))
        maxs.append(dr.split_percentile(user_df,'Full',0.95))
        mins.append(dr.split_extremes(user_df,'Full','min'))
    
    angles = []
    points = []
    outers = []

    quarters = []
    halfs = []    
    
    label_options = ['1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full']
    x_labels = []
    x_ticks = []
    
    for i in range(0,len(times)):
        
        base = maxs[i]
        outer = mins[i]
        split = times[i]
        
        quart = qs[i]
        half = hs[i]
        
        #print(base[-8:])
        
        base = datetime.strptime(base[-8:],'%H:%M:%S')
        outer = datetime.strptime(outer[-8:],'%H:%M:%S')
        split = datetime.strptime(split[-8:],'%H:%M:%S')
        
        quart = datetime.strptime(quart[-8:],'%H:%M:%S')
        half = datetime.strptime(half[-8:],'%H:%M:%S')
         
        full_diff = base - outer
        full_diff = full_diff.total_seconds()
        
        this_diff = split - outer
        this_diff = this_diff.total_seconds()
        
        try:
            fraction = this_diff/full_diff
        except:
            fraction = 1
        
        q_diff = quart - outer
        q_diff = q_diff.total_seconds()
        try:
            q_frac = 1 - q_diff/full_diff
        except:
            q_frac = 0
        
        h_diff = half - outer
        h_diff = h_diff.total_seconds()
        try:
            h_frac = 1 - h_diff/full_diff
        except:
            h_frac = 0
        
        point = 1 - fraction
        points.append(point)
        
        angle = 2 * pi * (i/len(times)) + pi/2
        angles.append(angle)
        
        outers.append(1)
        
        quarters.append(q_frac)
        halfs.append(h_frac)
        
        x_labels.append(label_options[i])
        x_ticks.append(angle)
        
    angles.append(angles[0])
    points.append(points[0])
    outers.append(1)
    
    quarters.append(quarters[0])
    halfs.append(halfs[0])
    
    #print(x_labels)
    #print(x_ticks)
    
    new_ticks = []
    
    for t in range(0,len(x_ticks)):
        if x_ticks[i] > pi * 2:
            new_ticks.append(x_ticks[i] - pi*2)
        else:
            new_ticks.append(x_ticks[i])
        
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    
    ax.plot(angles,points)
    ax.plot(angles,outers,':', color='red')
    ax.plot(angles,quarters,':', color='red')
    ax.plot(angles,halfs,':', color='red')
    
    
    new_x,new_lab = reorder_polar_labels(x_ticks, x_labels)
    #print(new_x)
    #print(new_lab)
    
    plt.xticks(new_x,new_lab)
    
    ax.set_thetamin(0)
    ax.set_thetamax(360)
        
#ws_df = dr.pull_data('WS')
#print('df pulled')s
#times_radar(ws_df,'4632607330')

def activity_tf(date_string,activity_type,user_df):
    dates = user_df['Date'].tolist()
    types = user_df['Activity Type'].tolist()
    
    found = False
    
    for i in range(0,len(dates)):
        if date_string in str(dates[i]) and activity_type in types[i]:
            found = True
            
    return(found)

def month_calendar(month,year,activity_type,user_df):
    title_activity = activity_type
    
    if activity_type == 'All':
        activity_type = 'i'
    
    first_day_string = f'{year}-{bf.add_zeros(month)}-01'
    f_d_strp = datetime.strptime(first_day_string,'%Y-%m-%d')
    f_d_deci = int(datetime.strftime(f_d_strp,'%u'))
    
    week_days = []
    temp_week_vals = []
    day_check = []
    
    for i in range(1,bf.month_length(month,year)+1):
        day_string = f'{year}-{bf.add_zeros(month)}-{bf.add_zeros(i)}'
        day_strp = datetime.strptime(day_string,'%Y-%m-%d')
        day_deci = int(datetime.strftime(day_strp,'%u'))
        week_days.append(day_deci)
        week = (i + f_d_deci - 2) // 7
        temp_week_vals.append(week)
        
        day_check.append(i)
    
    week_vals = []
    
    for i in range(0,len(temp_week_vals)):
        week_val = temp_week_vals[-1] - temp_week_vals[i]
        week_vals.append(week_val)   
    
    #print(month_length(month,year))
    #print(len(week_days))
    #print(day_check)
    
    for i in range(1,bf.month_length(month,year)+1):
        day_string = f'{year}-{bf.add_zeros(month)}-{bf.add_zeros(i)}'
        plot_val = activity_tf(day_string,activity_type,user_df)
        
        if plot_val == True:
            plt.scatter(week_days[i-1],week_vals[i-1],s=150,color='red')
        else:
            plt.scatter(week_days[i-1],week_vals[i-1],s=5,color='black')
            
        #print(week_days[i-1],week_vals[i-1])
        
    week_ticks = [1,2,3,4,5,6,7]
    week_labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    plt.xticks(week_ticks,week_labels)
    plt.ylim([-0.25,max(week_vals)+0.25])
    plt.yticks([-0.5],[''])
    
    plt.title(f'{title_activity}, {bf.month_caller(month)} {year}')
    
    
#ws_df = dr.pull_data('WS')
#print('df pulled')
#month_calendar(12,2020,'All',ws_df)

def plot_distances_this_year(user_df,m,yyyy,activity):
    #run_vals = []    
    
    title = '{} distances in {}'.format(activity,yyyy)
    
    if activity == 'All':
        activity = 'i' 
    
    #for i in range(0,len(dates)):
    #    if activity in types[i]:
    #        run_vals.append(i)
    #val = run_vals[0]
    
    fig,ax = plt.subplots()
    for i in range(1,m+1):
        temp_dates,temp_sum = month_dist_sum(i,yyyy,activity,user_df)
        temp_string = '{}: {}km'.format(bf.month_caller(i),round(temp_sum[-1],1))
        if i < 11:
            plt.plot(temp_dates,temp_sum,label=temp_string)
        elif i == 11:
            plt.plot(temp_dates,temp_sum,label=temp_string,color='deeppink')
        elif i == 12:
            plt.plot(temp_dates,temp_sum,label=temp_string,color='lime')
    
    if m+1 >=6:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        ax.legend();
    
    plt.title(title)
    
def plotly_distances_this_year_and_last(user_df,m,yyyy,activity):
    
    user_df = user_df[user_df['Activity Type'].isin([activity])]
    
    abs_m = m
    
    fig = go.Figure()
    
    def create_empty(m,yyyy):
        
        month_length = bf.month_length(m,yyyy)
        
        l = [str(int(x)) for x in range(0,month_length+1)]
        
        df = pd.DataFrame.from_dict({'day': l})
        
        return df
    
    def plot_month(user_df,m,yyyy, present_year = True):
        
        user_df['year'] = user_df['Date'].apply(lambda x: float(x[:4]))
        user_df = user_df[user_df['year']==yyyy]
        user_df['month'] = user_df['Date'].apply(lambda x: float(x[5:7]))
        user_df = user_df[user_df['month']==m]
        
        user_df['day'] = user_df['Date'].apply(lambda x: str(int(float(x[8:10]))))
        
        user_df = user_df[['day','Distance']]
        
        month_df = pd.merge(create_empty(m, yyyy),user_df,how='outer',on='day')
        month_df['Distance'] = month_df['Distance'].fillna(0)
        month_df['Distance Covered'] = month_df['Distance'].cumsum()
        
        colours_dict = {
            '1': 'blue',
            '2': 'red',
            '3': 'purple',
            '4': 'coral',
            '5': 'olivedrab',
            '6': 'fuchsia',
            '7': 'black',
            '8': 'gold',
            '9': 'grey',
            '10': 'cyan',
            '11': 'deeppink',
            '12': 'lime'
            }
        
        colour = colours_dict.get(str(int(m)))
        line_style = 'solid' if present_year else 'dash'
        if present_year:
            visibility = True
        elif abs_m <= 3 and m <= 3:
            visibility = True
        else:
            visibility = 'legendonly'
        
        fig.add_trace(
            go.Scatter(
                mode='lines',
                name=f'{bf.month_caller(m)} {yyyy}',
                x=month_df['day'],
                y=month_df['Distance Covered'],
                line={'color': colour,
                      'dash': line_style},
                #hovertemplate = hover_t,
                visible=visibility,
                showlegend = True
                ))
    
    for mm in range(1,m+1):
        plot_month(user_df,mm,yyyy)
        
    for mm in range(1,13):
        plot_month(user_df,mm,yyyy-1,present_year=False)
        
    fig.update_layout(title=f'Monthly {activity} Distances in {yyyy} (and {int(yyyy-1)})',
                xaxis=dict(showgrid=False),
              yaxis=dict(title='km')
)

        
    div = pio.to_html(fig,auto_play=False,full_html=False)
    
    return div

def interpret_rankings(rankings, desired_distance=None):
        
        rankings = json.loads(rankings.replace("'", '"'))
        if rankings:
            #raise ValueError(rankings, type(rankings))
            
            r = '' 
            
            links = {
                '1st': 	'&#129351',
                    #'<img src="https://img.icons8.com/color-glass/48/000000/trophy.png"/>',
                '2nd': '&#129352;',
                    #'''<img src="https://d3nn82uaxijpm6.cloudfront.net/assets/svg/icon-at-pr-02-dced92d045c9ba151bd5540df94ae376351f1fc8707cd91d587aef2a221ad726.svg"
#style="height: 50%; overflow: hidden; transform: translateY(-50%);"/>''',
                '3rd': '&#129353;'
                    #'<img src="https://img.icons8.com/color-glass/48/000000/trophy.png"/>'
                }
            
            for p in ('1st', '2nd', '3rd'):
                l = rankings.get(p, [])
                
                if desired_distance:
                    l = [r for r in l if r == desired_distance]
                    
                if l:
                    r += links[p] * len(l)
            
            return r
            
        else:
            return ''
    
    
def rankings_html(user_df,distance):
    
    user_df = user_df.loc[user_df['Activity Type'] == 'Running']
    
    user_df = user_df.loc[user_df[distance] != 'NONE']
    
    user_df = user_df.sort_values(by=[distance,'Date'],ascending=True)
    
    ac_nos = user_df['Activity number'].tolist()
    ac_dates = user_df['Date'].tolist()
    times = user_df[distance].tolist()
    
    user_df['split'] = user_df[distance].apply(bf.split_to_floatminute)
    dist = dr.dist_dict[distance]/1000
    user_df['pace'] = user_df['split'] / dist
    user_df['pace'] = user_df['pace'].apply(bf.floatminute_to_stringtime)
    paces = user_df['pace'].tolist()
    notes = user_df['Notes'].fillna('').tolist()
    run_rankings = user_df['Run Rankings'].tolist()
    
    ranks = [1]
    
    for i in range(1,len(times)):
        
        if times[i] == times[i-1]:
            ranks.append(ranks[-1])
        else:
            ranks.append(i+1)
    #this is used to rank splits
    #you could use a groupby and a count and then merge in, if you wanted
    
    times = list(map(lambda x: str(x).replace('0 days ',''), times))
    durl = bf.dtag_to_durl(distance)
         
    html = '''<th>Rank</th><th>Date</th><th>Split</th><th>Pace (m/km)</th><th>Notes</th><th></th>'''

    for i in range(0, len(ac_nos)):
        row = f"""<tr>
<td>{ranks[i]}</td>
<td><a href='../index/{ac_nos[i]}'>{ac_dates[i]}</a></td>
<td><a href='../index/{ac_nos[i]}/map/{durl}'>{times[i]}</a></td>
<td>{paces[i]}</td>
<td>{notes[i]}</td>
<td>{interpret_rankings(run_rankings[i], distance)}
</tr>"""#could link to split map

#there is a much neater solution here, whereby

        html = html + row
        
        #'&#129351'
        
    return(html)

def top_n(user_df,n=3):
    
    full = ''
    
    for i in range(0,len(dr.dist_list)):
        
        distance = dr.dist_list[i]
        
        durl = bf.dtag_to_durl(distance)
    
        user_df = user_df.loc[user_df['Activity Type'] == 'Running']
    
        user_df = user_df.loc[user_df[distance] != 'NONE']
    
        user_df = user_df.sort_values(by=[distance,'Date'],ascending=True)
    
        ac_nos = user_df['Activity number'].tolist()
        ac_dates = user_df['Date'].tolist()
        times = user_df[distance].tolist()
    
        html = f'<b><u>{distance}</u></b><br>'

        for v in range(0, n):
            try:
                row = f"""
<a href='../index/{ac_nos[v]}/map/{durl}'>{str(times[v])[-8:]}</a>, <a href='../index/{ac_nos[v]}'>{ac_dates[v]}</a><br>
"""
            except:
                row = ''

            html = html + row
            
        if distance == '1 mile':
            dist = '1mile'
        elif distance == '1.5 mile':
            dist = '1.5mile'
        elif distance == '3 mile':
            dist = '3mile'
        else:
            dist = distance
            
        full = full + html + f"""<a href='/rankings/{dist}'>Full rankings</a><br>"""
        
    return(full)

def formatted_title(title):
    
    t = bf.durl_to_dtag(title)
    
    return(t)

def convert_date_to_abs(date):
    
    sec = date.total_seconds()
    
    return(sec)

def convert_split_to_floatminute(split):
    
    string = str(split)[-8:]
    
    mins = bf.stringtime_to_floatminute(string)
    
    return(mins)

def splits_plot(user_df,split):
    df = user_df
    dist = formatted_title(split)
    
    df = df.loc[df['Activity Type'] == 'Running']
    df = df.loc[df[dist] != 'NONE']
    
    df['seconds'] = df['Date'].apply(bf.convert_time)
    df['split'] = df[dist].apply(convert_split_to_floatminute)
    
    mean = (df['split'].mean())
    std = (df['split'].std())
    
    df = df.loc[df['split'] < mean + 2.5*std]
    
    plt.scatter(df['seconds'], df['split'])
    
    plt.title(dist)
    
def times_curve(user_df,ac_no):
    
    #user_df = user_df[]
    
    times = [0]
    points = [0]
    tags = ['0km']
    
    fig,ax = plt.subplots()
    
    for i in range(0, len(dr.dist_list)):
        split = dr.activity_splits(user_df,ac_no,dr.dist_list[i])
        if split != 'NONE':
            t = bf.stringtime_to_floatminute(str(split)[-8:])
            times.append(t)
            points.append(dr.dist_dict[dr.dist_list[i]])
            tags.append(dr.dist_list[i])
            
    full_d = dr.activity_details(user_df,ac_no,'Distance')
    full_t = dr.activity_details(user_df,ac_no,'Time')
    #raise ValueError(full_t)
    full_t = bf.stringtime_to_floatminute(str(full_t)[-8:])
    
    times.append(full_t)
    points.append(full_d * 1000)
    tags.append(f'{full_d}km')
            
    #print(times)        
            
    plt.plot(points,times,':.')
    
    plt.xticks(points,tags)
    
def all_splits_plot(user_df,options='all'):
    
    user_df = bf.running_filter(user_df)
    
    fig = go.Figure()
    
    if options == 'all':
        for i in range(0,len(dr.dist_list)):
            d = dr.dist_list[i]
        
            d_df = user_df.loc[user_df[d] != 'NONE']
        
            d_df[d] = d_df[d].apply(bf.split_to_dt)
        
            hover_t = '''%{x}<extra></extra>'''
        
            fig.add_trace(
                go.Scatter(
                    name=d,
                    mode='markers',
                    x=d_df['Date'],
                    y=d_df[d],
                    hovertemplate = hover_t,
                    showlegend = True
                    ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Time",
            yaxis=dict(
                range=[bf.split_to_dt('00:00:00'), bf.split_to_dt('01:00:00')]
                ))
        
        div = pio.to_html(fig,auto_play=False,full_html=False)
        
    else:
        d = options
        
        d_df = user_df.loc[user_df[d] != 'NONE']
        
        d_df[d] = d_df[d].apply(bf.split_to_dt)
        
        hover_t = '''%{x}<extra></extra>'''
        
        fig.add_trace(
                go.Scatter(
                    mode='markers',
                    name='Times',
                    x=d_df['Date'],
                    y=d_df[d],
                    hovertemplate = hover_t,
                    showlegend = True
                    ))
        
        #d_df[d] = pd.to_numeric(d_df[d])
        mean = (d_df[d].mean())
        m = f'{bf.add_zeros(str(mean.hour))}:{bf.add_zeros(str(mean.minute))}:{bf.add_zeros(str(mean.second))}'
        m_t = bf.stringtime_to_floatminute(m)
        lim_t = m_t * 1.5
        lim_t = bf.floatminute_to_stringtime(lim_t)
        
        #print(lim_t)
        #lim = mean + datetime.strptime(var, '%H:%M:%S')
        
        #print(type(lim))
        #print(d_df[d].std())
        
        best = d_df[d].tolist()[0]
        times = {d_df['Date'].tolist()[0]: {'time': best}}
        
        bests = [bf.split_to_dt(d_df['Time'].tolist()[0])]
        dates = [d_df['Date'].tolist()[0]]
        
        #for d,t in zip(d_df['Date'].tolist(), d_df['Time'].tolist()):
        #    if bf.split_to_dt(t) < best:
        #        best = bf.split_to_dt(t)
        #        times[d] = {'time': best}
        
        for d,t in zip(d_df['Date'].tolist(), d_df[d].tolist()):
            #time = bf.split_to_dt(t)
            if t < bests[-1]:
                if len(bests) > 1:
                    bests.append(bests[-1])
                    dates.append(d)
                bests.append(t)
                dates.append(d)
                
        bests.append(bests[-1])
        dates.append(d_df['Date'].tolist()[-1])
                
        #lastday = d_df['Date'].tolist()[-1]
        #durations = []
        
        for d in range(len(times)):
            this_day = list(times.keys())[d]
            next_day = list(times.keys())[d+1] if d < len(times)-1 else d_df['Date'].tolist()[-1]
            #raise ValueError(this_day, next_day)
            try:
                diff = datetime.strptime(next_day, '%Y-%m-%d %H:%M:%S') - datetime.strptime(this_day, '%Y-%m-%d %H:%M:%S')
            except:
                raise ValueError(next_day, this_day)
            width = diff
            times[this_day]['held_for'] = diff.days
            times[this_day]['width'] = width         
            diff = diff.days
            midpoint = datetime.strptime(this_day, '%Y-%m-%d %H:%M:%S') + relativedelta.relativedelta(days=int(diff/2))
            times[this_day]['midpoint'] = midpoint
            
        #bests = [i['time'] for i in list(times.values())]
        #points = [i['midpoint'] for i in list(times.values())]
        #widths = [i['width'].days for i in list(times.values())]
        
        fig.add_trace(
                go.Scatter(
                    name='Best',
                    mode='lines',
                    x=dates,
                    y=bests,
                    #width=widths,
                    #hovertemplate = hover_t,
                    showlegend = True
                    ))
            
        #raise ValueError(times)    
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Time",
            yaxis=dict(
                range=[bf.split_to_dt('00:00:00'), bf.split_to_dt(lim_t)]
                ))
        
        div = pio.to_html(fig,auto_play=False,full_html=False,default_width='60%')
    
    return(div)
        
    
        
"""    
    fig = go.Figure()
    
    fig.add_trace(
    go.Scatter(
        mode='markers',
        x=base_df['Distance'],
        y=base_df['Time'],
        #text = base_df['Date'],
        marker=dict(
            color='Blue'
            ),
        hovertemplate = hover_t,
        text = ['{}'.format(i) for i in range(len(base_df))],
        showlegend = False,
        
        )
    )
"""  

def prev_next(ac_no,user_df):
    
    date = dr.activity_details(user_df,ac_no,'Date')
    
    try:
        prev_df = user_df.loc[user_df['Date'] < date]
        prev_date = prev_df['Date'].tolist()[-1]
        prev_ac = prev_df['Activity number'].tolist()[-1]
        
        prev_string = f"<a href='../{prev_ac}'>{prev_date}</a> | "
        
    except:
        prev_string = ''
    
    try:
        post_df = user_df.loc[user_df['Date'] > date]
        post_date = post_df['Date'].tolist()[0]
        post_ac = post_df['Activity number'].tolist()[0]
    
        post_string = f" | <a href='../{post_ac}'>{post_date}</a>"
    except:
        post_string = ''
    
    string = f'{prev_string}{date}{post_string}'
    
    return (string)
    
def distances_covered_list(user_df,ac_no):
    
    distance = dr.activity_details(user_df,ac_no,'Distance') * 1000
    
    distances = []
    
    for i in range(0,len(dr.dist_list)):
        if dr.dist_dict[dr.dist_list[i]] < distance:
            distances.append(dr.dist_list[i])
            
    return(distances)

def distances_options(user_df,ac_no):
    
    distances = distances_covered_list(user_df,ac_no)
    
    html = ''
    
    for i in range(0,len(distances)):
        durl = bf.dtag_to_durl(distances[i])
        line = f"""<a href='{durl}'>{distances[i]}</a>: {dr.activity_splits(user_df,ac_no,str(distances[i]))[-8:]}
"""

        if i != len(distances) - 1:
            line = line + '<br>'
            
        html = html + line
        
    return(html)
        


    