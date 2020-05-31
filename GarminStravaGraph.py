#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 09:39:30 2020

@author: WS
"""

import pandas as pd
import matplotlib.pyplot as plt

"""Garmin Connect -> Activities -> All Activities  
    -> (Scroll down to include all) -> Export -> (Move to correct location)"""
    
data = pd.read_csv (r'Activities.csv')   
df = pd.DataFrame(data, columns= ['Activity Type','Date','Distance','Time'])

#makes dates useable
dates_times = df['Date'].tolist()
dates = []
for i in range(0,len(dates_times)):
    useful_dates = dates_times[i][0:10]
    dates.append(useful_dates)

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

dates.reverse()
distances.reverse()
durations.reverse()
types.reverse()
#ensures chronological order, as cannot sort all activities - might want an if check here

def date_string(m,yyyy):
    if m == 10 or m == 11 or m == 12:
        string = '{}-{}'.format(yyyy,m)
    else:
        string = '{}-0{}'.format(yyyy,m)
    return(string)

def distance_sum(m,yyyy):
    sum_distances = [0]
    month_dates = [0]
    
    for i in range(0,len(dates)):
        if date_string(m,yyyy) in dates[i] and 'Running' in types[i]:
            dist = round(sum_distances[-1] + float(distances[i]),2)
            sum_distances.append(dist)
            month_dates.append(float(dates[i][-2:]))
    
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
    mins_string = time_string(minutes)
    secs_string = round(seconds * 60)
    
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
    
    #error message?
    return(month_dates,plot_mins)
    
def populate_arrays(m,yyyy,month_dates,curr_vals):
    count = 0  
    lim = month_length(m,yyyy)
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
    """
    for i in range(0,month_length(m,yyyy)):
        if round(month_dates[-1]) == round(month_dates[i]):
            month_dates.append(i+1)
            curr_vals.append(curr_vals[-1])
        elif round(month_dates[i + 1]) != i + 1:
            month_dates.insert(i + 1,i + 1)
            curr_vals.insert(i + 1,curr_vals[i])
    """
    
"""
Complete Functions
"""
    
def plot_month_and_previous_distances(m,yyyy):
    curr_month_dates, curr_sum_distances = distance_sum(m,yyyy)
    populate_arrays(m,yyyy,curr_month_dates,curr_sum_distances)
    
    if m == 1:
        new_year = yyyy - 1 
        prev_month_dates, prev_sum_distances = distance_sum(12,new_year)
        populate_arrays(12,new_year,prev_month_dates,prev_sum_distances)
    else:
        prev_month_dates, prev_sum_distances = distance_sum((m-1),yyyy)
        populate_arrays((m-1),yyyy,prev_month_dates,prev_sum_distances)
    
    junk_month_dates,prev_mins = duration_sum(m-1,yyyy)
    prev_annot = '{} {}: {}km in {} '.format(month_caller(m-1),yyyy,round(prev_sum_distances[-1]),floatminute_to_stringtime(prev_mins[-1]))
    
    junk_month_dates,curr_mins = duration_sum(m,yyyy)
    curr_annot = '{} {}: {}km in {} '.format(month_caller(m),yyyy,round(curr_sum_distances[-1]),floatminute_to_stringtime(curr_mins[-1]))
    
    plt.plot(prev_month_dates, prev_sum_distances,color='blue')
    plt.text(prev_month_dates[-2],prev_sum_distances[-1],prev_annot,horizontalalignment='right')
    plt.plot(curr_month_dates, curr_sum_distances,color='red')
    plt.text(curr_month_dates[-2],curr_sum_distances[-1],curr_annot,horizontalalignment='right')
    
def plot_month_and_previous_durations(m,yyyy):
    curr_month_dates, curr_sum_durs = duration_sum(m,yyyy)
    populate_arrays(m,yyyy,curr_month_dates,curr_sum_durs)
    if m == 1:
        new_year = yyyy - 1 
        prev_month_dates, prev_sum_durs = duration_sum(12,new_year)
        populate_arrays(m,new_year,prev_month_dates,prev_sum_durs)
    else:
        prev_month_dates, prev_sum_durs = duration_sum((m-1),yyyy)
        populate_arrays((m-1),yyyy,prev_month_dates,prev_sum_durs)
    
    junk_month_dates,prev_dists = distance_sum(m-1,yyyy)
    prev_annot = '{} {}: {}km in {} '.format(month_caller(m-1),yyyy,round(prev_dists[-1]),floatminute_to_stringtime(prev_sum_durs[-1]))
    
    junk_month_dates,curr_dists = distance_sum(m,yyyy)
    curr_annot = '{} {}: {}km in {} '.format(month_caller(m),yyyy,round(curr_dists[-1]),floatminute_to_stringtime(curr_sum_durs[-1]))
    
    plt.plot(prev_month_dates, prev_sum_durs,color='blue')
    plt.text(prev_month_dates[-2],prev_sum_durs[-1],prev_annot,horizontalalignment='right')
    plt.plot(curr_month_dates, curr_sum_durs,color='red')
    plt.text(curr_month_dates[-2],curr_sum_durs[-1],curr_annot,horizontalalignment='right')
    
#plot_month_and_previous_durations(4,2020)

from time import time, ctime, localtime

t = time()
print_time = ctime(t)
print(print_time)

now = list(localtime(t))
year = now[0]
month = now[1]

plot_month_and_previous_distances(month,year)
plt.show()
plot_month_and_previous_durations(month,year)
plt.show()