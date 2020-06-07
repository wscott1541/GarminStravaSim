#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 09:39:30 2020

@author: WS
"""

import pandas as pd
import matplotlib.pyplot as plt

from time import time, localtime
from datetime import datetime

t = time()

now = list(localtime(t))
year = now[0]
month = now[1]
day = now[2]

def add_zeros(number):
    if float(number) >= 10:
        string = number
    else:
        string = '0{}'.format(number)
    return(string)
    
today_string = '{}-{}-{}'.format(year,add_zeros(month),add_zeros(day))

    
data = pd.read_csv(r'Activities.csv')   
df = pd.DataFrame(data, columns= ['Activity Type','Date','Distance','Time'])
df = df.sort_values(by='Date')#sort_values is deprecated Python

#print(df)

#makes dates useable
dates_times = df['Date'].tolist()
dates = []
for i in range(0,len(dates_times)):
    useful_dates = dates_times[i][0:10]
    dates.append(useful_dates)#in format string 'yyyy-mm-dd'

"""    
from datetime import datetime
new_dates = []
for i in range(0,len(dates)):
    datetime_strp = datetime.strptime(dates_times[i],'%Y-%m-%d %H:%M:%S')
    datetime_object = datetime.timestamp(datetime_strp)
    new_dates.append(datetime_object)
df['New_dates'] = new_dates

df.sort_values(by='New_dates',ascending=True)
"""


#make distances useable
distances = df['Distance'].tolist()

#make durations useable
#duration_times = df['Time'].tolist()
duration_strings = df['Time'].tolist()

def stringtime_to_floatminute(time_string):
    hours = float(time_string[:2])
    minutes = float(time_string[3:5])
    seconds = float(time_string[6:8])
    
    time = hours * 60 + minutes + seconds/60
    
    return(time)
    
durations = []
for i in range(0,len(duration_strings)):
    dur = stringtime_to_floatminute(duration_strings[i])
    durations.append(dur)
    
#make times useable
types = df['Activity Type'].tolist()

"""
dates.reverse()
distances.reverse()
durations.reverse()
types.reverse()
"""
#ensures chronological order, as cannot sort all activities - might want an if check here
#Potentially try to sort by date before stripping out to list

def date_string(m,yyyy):
    if m == 10 or m == 11 or m == 12:
        string = '{}-{}'.format(yyyy,m)
    else:
        string = '{}-0{}'.format(yyyy,m)
    return(string)

def datestring_to_floatmonth(datestring):
    year = round(float(datestring[:4]))
    month = round(float(datestring[5:7]))
    
    new = year * 12 + month
    
    return(new)

def pull_month_and_year(datestring):
    m = round(float(datestring[5:7]))
    yyyy = round(float(datestring[:4]))
    return(m,yyyy)
    
def floatmonth_to_datestring(floatmonth):
    new = divmod(floatmonth,12)
    new_year = new[0]
    new_month = new[1]
    if new_month == 0:
        new_year = new_year - 1
        new_month = 12
    string = date_string(new_month,new_year)
    return(string)
    
def populate_arrays(m,yyyy,month_dates,curr_vals):
    lim = month_length(m,yyyy)
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

def distance_sum(m,yyyy):
    sum_distances = [0]
    month_dates = [0]
    
    for i in range(0,len(dates)):
        if date_string(m,yyyy) in dates[i] and 'Running' in types[i]:
            dist = round(sum_distances[-1] + float(distances[i]),2)
            sum_distances.append(dist)
            month_dates.append(float(dates[i][-2:]))
    
    populate_arrays(m,yyyy,month_dates,sum_distances)
    
    #error message?
    return(month_dates,sum_distances)
    
def month_caller(m):
    if m == 1:
        string = 'Jan'
    if m == 2:
        string = 'Feb'
    if m == 3:
        string = 'Mar'
    if m == 4:
        string = 'Apr'
    if m == 5:
        string = 'May'
    if m == 6:
        string = 'Jun'
    if m == 7:
        string = 'Jul'
    if m == 8:
        string = 'Aug'
    if m == 9:
        string = 'Sep'
    if m == 10:
        string = 'Oct'
    if m == 11:
        string = 'Nov'
    if m == 12:
        string = 'Dec'
    return(string)

def month_length(m,yyyy):
    if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
        length = 31
    if m == 4 or m == 6 or m == 9 or m == 11:
        length = 30
    if m == 2 and yyyy == 2016:
        length = 29
    elif m == 2 and yyyy == 2020:
        length = 29
    elif m == 2:
        length = 28
        
    if m == month and yyyy == year:
        length = day
    
    return(length)

def time_string(n):
    if n < 10:
        string = '0{}'.format(round(n))
    else:
        string = '{}'.format(round(n))
    return(string)
    
def floatminute_to_stringtime(time):
    hours_calc = list(divmod(time,60))
    hours = hours_calc[0]
    remaining = hours_calc[1]
    mins_calc = list(divmod(remaining,1))
    minutes = mins_calc[0]
    seconds = mins_calc[1]
    
    hour_string = time_string(hours)
    mins_string = add_zeros(time_string(minutes))
    secs_string = add_zeros(round(seconds * 60))
    
    string = '{}:{}:{}'.format(hour_string,mins_string,secs_string)
    
    return(string)

"""
def add_times(a,b):
    #requires times in minutes, or at least same units

    time = a_mins + b_mins
    
    return(time)
"""
        
def duration_sum(m,yyyy):
    plot_mins = [0]
    month_dates = [0]
    
    for i in range(0,len(dates)):
        if date_string(m,yyyy) in dates[i] and 'Running' in types[i]:
            times = plot_mins[-1] + durations[i]
            plot_mins.append(times)
            month_dates.append(float(dates[i][-2:]))
            
    populate_arrays(m,yyyy,month_dates,plot_mins)
    
    #error message?
    return(month_dates,plot_mins)
        
def month_diff(m1,yyyy1,m2,yyyy2):
    mon1 = yyyy1 * 12 + m1
    mon2 = yyyy2 * 12 + m2
    diff = mon1 - mon2
    return(diff)
    
def datestring_to_floatday(datestring):
    d = round(float(datestring[8:]))
    m = round(float(datestring[5:7]))
    yyyy = round(float(datestring[:4]))
    
    floatday = yyyy * 364 + month_length(m,yyyy) + d
    
    return(floatday)
    #I have four years to code for leap years
"""
Complete Functions
"""
    
def plot_month_and_previous_distances(m,yyyy):
    curr_month_dates, curr_sum_distances = distance_sum(m,yyyy)
    
    if m == 1:
        new_year = yyyy - 1 
        prev_month_dates, prev_sum_distances = distance_sum(12,new_year)
    else:
        prev_month_dates, prev_sum_distances = distance_sum((m-1),yyyy)
    
    junk_month_dates,prev_mins = duration_sum(m-1,yyyy)
    prev_annot = '{} {}: {}km in {} '.format(month_caller(m-1),yyyy,round(prev_sum_distances[-1]),floatminute_to_stringtime(prev_mins[-1]))
    
    junk_month_dates,curr_mins = duration_sum(m,yyyy)
    curr_annot = '{} {}: {}km in {} '.format(month_caller(m),yyyy,round(curr_sum_distances[-1]),floatminute_to_stringtime(curr_mins[-1]))
    
    fig,ax = plt.subplots()
    plt.plot(prev_month_dates, prev_sum_distances,color='blue',label = prev_annot)
    #plt.text(prev_month_dates[-2],prev_sum_distances[-1],prev_annot,horizontalalignment='right')
    plt.plot(curr_month_dates, curr_sum_distances,color='red', label = curr_annot)
    #plt.text(curr_month_dates[-2],curr_sum_distances[-1],curr_annot,horizontalalignment='right')
    ax.legend();
    
def plot_month_and_previous_durations(m,yyyy):
    curr_month_dates, curr_sum_durs = duration_sum(m,yyyy)
    if m == 1:
        new_year = yyyy - 1 
        prev_month_dates, prev_sum_durs = duration_sum(12,new_year)
    else:
        prev_month_dates, prev_sum_durs = duration_sum((m-1),yyyy)
    
    junk_month_dates,prev_dists = distance_sum(m-1,yyyy)
    prev_annot = '{} {}: {}km in {} '.format(month_caller(m-1),yyyy,round(prev_dists[-1]),floatminute_to_stringtime(prev_sum_durs[-1]))
    
    junk_month_dates,curr_dists = distance_sum(m,yyyy)
    curr_annot = '{} {}: {}km in {} '.format(month_caller(m),yyyy,round(curr_dists[-1]),floatminute_to_stringtime(curr_sum_durs[-1]))
    
    fig,ax = plt.subplots()
    plt.plot(prev_month_dates, prev_sum_durs,color='blue',label=prev_annot)
    #plt.text(prev_month_dates[-2],prev_sum_durs[-1],prev_annot,horizontalalignment='right')
    plt.plot(curr_month_dates, curr_sum_durs,color='red',label=curr_annot)
    #plt.text(curr_month_dates[-2],curr_sum_durs[-1],curr_annot,horizontalalignment='right')
    ax.legend();
    
def plot_durations_all_previous(m,yyyy):
    run_vals = []    
    for i in range(0,len(dates)):
        if 'Running' in types[i]:
            run_vals.append(i)
    val = run_vals[0]
    earliest_date = dates[val]
    
    pick_month = yyyy * 12 + m
    earl_month = datestring_to_floatmonth(earliest_date)
    
    fig,ax = plt.subplots()
    for i in range(earl_month,pick_month+1):
        temp_datestring = floatmonth_to_datestring(i)
        m_val,yyyy_val = pull_month_and_year(temp_datestring)
        temp_dates,temp_sum = duration_sum(m_val,yyyy_val)
        plt.plot(temp_dates,temp_sum,label=temp_datestring)
    ax.legend();
    
def plot_distances_all_previous(m,yyyy):
    run_vals = []    
    for i in range(0,len(dates)):
        if 'Running' in types[i]:
            run_vals.append(i)
    val = run_vals[0]
    earliest_date = dates[val]
    
    pick_month = yyyy * 12 + m
    earl_month = datestring_to_floatmonth(earliest_date)
    
    fig,ax = plt.subplots()
    for i in range(earl_month,pick_month+1):
        temp_datestring = floatmonth_to_datestring(i)
        m_val,yyyy_val = pull_month_and_year(temp_datestring)
        temp_dates,temp_sum = distance_sum(m_val,yyyy_val)
        plt.plot(temp_dates,temp_sum,label=temp_datestring)
    ax.legend();
    
def plot_cumulative_distance(m,yyyy):
    run_vals = []    
    for i in range(0,len(dates)):
        if 'Running' in types[i]:
            run_vals.append(i)
    val = run_vals[0]
    earliest_date = dates[val]
    
    pick_month = yyyy * 12 + m
    earl_month = datestring_to_floatmonth(earliest_date)
    
    cum_dates = [0]
    cum_dist = [0]
    
    fig,ax = plt.subplots()
    for i in range(earl_month,pick_month+1):
        temp_datestring = floatmonth_to_datestring(i)
        m_val,yyyy_val = pull_month_and_year(temp_datestring)
        temp_dates,temp_sum = distance_sum(m_val,yyyy_val)
        prec_len = cum_dates[-1]+1
        prec_dist = cum_dist[-1]
        plot_dates = []
        plot_dist = []
        for val in range(0,len(temp_dates)):
            cum_dates.append(temp_dates[val]+prec_len)
            plot_dates.append(temp_dates[val]+prec_len)
            cum_dist.append(temp_sum[val]+prec_dist)
            plot_dist.append(temp_sum[val]+prec_dist)
        plt.plot(plot_dates,plot_dist,label=temp_datestring)
    ax.legend();

def populate_arrays_generic(lim,days,vals):
    
    if days[-1] < lim:
        days.append((days[-1]) + 1)
        vals.append(vals[-1])
    count = 0
    i = 0      
    while i < lim:
        if days[i] == days[-1] and days[i] != lim:
            days.append(i+1-count)
            vals.append(vals[-1])
        elif days[i] == days[i+1]:
            count += 1
            lim += 1
        elif days[i + 1] != i + 1 - count:
            days.insert(i + 1,i + 1 - count)
            vals.insert(i + 1,vals[i])  
        i += 1

def distance_sum_curr_week(today_string):
    date_strp = datetime.strptime(today_string,'%Y-%m-%d')
    date_object = datetime.timestamp(date_strp)
    
    sum_distances = [0]
    week_dates = [0]
    
    for i in range(1,8):
        temp_date_object = date_object - (24 * 60 * 60) * ((7-i))
        temp_date_dt = datetime.fromtimestamp(temp_date_object)
        temp_date_string = datetime.strftime(temp_date_dt,'%Y-%m-%d')
        print(temp_date_string)
        
        for d in range (0,len(dates)):
            if temp_date_string in dates[d] and 'Running' in types[d]:
                dist = round(sum_distances[-1] + float(distances[d]),2)
                sum_distances.append(dist)
                week_dates.append(i)
   
    populate_arrays_generic(7,week_dates,sum_distances)
    
    if week_dates[1] == 0:
        sum_distances.remove(sum_distances[0])
        week_dates.remove(week_dates[0])
    
    #error message?
    return(week_dates,sum_distances)

def distance_sum_prev_week(today_string):
    date_strp = datetime.strptime(today_string,'%Y-%m-%d')
    date_object = datetime.timestamp(date_strp) - 24 * 60 * 60 * 7
    
    sum_distances = [0]
    week_dates = [0]
    
    for i in range(1,8):
        temp_date_object = date_object - (24 * 60 * 60) * ((7-i))
        temp_date_dt = datetime.fromtimestamp(temp_date_object)
        temp_date_string = datetime.strftime(temp_date_dt,'%Y-%m-%d')
        
        for d in range (0,len(dates)):
            if temp_date_string in dates[d] and 'Running' in types[d]:
                dist = round(sum_distances[-1] + float(distances[d]),2)
                sum_distances.append(dist)
                week_dates.append(i)
   
    populate_arrays_generic(7,week_dates,sum_distances)
    
    if week_dates[1] == 0:
        sum_distances.remove(sum_distances[0])
        week_dates.remove(week_dates[0])
    
    #error message?
    return(week_dates,sum_distances)
  
def plot_week_and_previous_distances(today_string):
   tw_dates,tw_dist = distance_sum_curr_week(today_string)
   this_annot = 'This week: {}km'.format(tw_dist[-1])
   
   pw_dates,pw_dist = distance_sum_prev_week(today_string)
   prev_annot = 'Last week: {}km'.format(pw_dist[-1])
   
   fig,ax = plt.subplots()
   plt.plot(pw_dates, pw_dist,color='blue',label=prev_annot)
   
   plt.plot(tw_dates, tw_dist,color='red',label=this_annot)
   
   ax.legend(); 





