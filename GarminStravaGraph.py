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
durations = df['Time'].tolist()
#for i in range(0,len(duration_times)):
#    dur = dt.datetime.strptime(duration_times[i],'%H:%M:%S')
#    useful_dur = dt.timedelta(hours=dur.hour, minutes=dur.minute, seconds=dur.second)
#    durations.append(useful_dur)
    
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
    
def plot_month_and_previous_distances(m,yyyy):
    curr_month_dates, curr_sum_distances = distance_sum(m,yyyy)
    if m == 1:
        new_year = yyyy - 1 
        prev_month_dates, prev_sum_distances = distance_sum(12,new_year)
    else:
        prev_month_dates, prev_sum_distances = distance_sum((m-1),yyyy)
    
    plt.plot(prev_month_dates, prev_sum_distances,color='blue')
    plt.plot(curr_month_dates, curr_sum_distances,color='red')

def time_string(n):
    if n < 10:
        string = '0{}'.format(round(n))
    else:
        string = '{}'.format(round(n))
    return(string)

def add_times(a,b):
    #only works for times < 100 hours - error message?
    hours_a = float(a[:2])
    minutes_a = float(a[3:5])
    seconds_a = float(a[6:8])
    
    hours_b = float(b[:2])
    minutes_b = float(b[3:5])
    seconds_b = float(b[6:8])
    
    sec_calc = list(divmod(seconds_a + seconds_b,60))
    extra_minutes = sec_calc[0]
    new_seconds = sec_calc[1]
    
    min_calc = list(divmod((minutes_a + minutes_b + extra_minutes),60))
    extra_hours = min_calc[0]
    new_minutes = min_calc[1]
    
    new_hours = hours_a + hours_b + extra_hours
    
    total_minutes = (new_hours*60) + new_minutes + (new_seconds/60)
    
    hour_string = time_string(new_hours)
    minute_string = time_string(new_minutes)
    second_string = time_string(new_seconds)
    new_string = '{}:{}:{}'.format(hour_string,minute_string,second_string)
    
    return(total_minutes,new_string)
        
def duration_sum(m,yyyy):
    plot_mins = [0]
    times = ['00:00:00']
    month_dates = [0]
    
    for i in range(0,len(dates)):
        if date_string(m,yyyy) in dates[i] and 'Running' in types[i]:
            mins,times_string = add_times(times[-1],durations[i])
            plot_mins.append(mins)
            times.append(times_string)
            month_dates.append(float(dates[i][-2:]))
            
    total_string = times[-1]
    
    #error message?
    return(month_dates,plot_mins,total_string)
    
def plot_month_and_previous_durations(m,yyyy):
    curr_month_dates, curr_sum_durs,curr_total = duration_sum(m,yyyy)
    if m == 1:
        new_year = yyyy - 1 
        prev_month_dates, prev_sum_durs,prev_total = duration_sum(12,new_year)
    else:
        prev_month_dates, prev_sum_durs,prev_total = duration_sum((m-1),yyyy)
    
    plt.plot(prev_month_dates, prev_sum_durs,color='blue')
    plt.plot(curr_month_dates, curr_sum_durs,color='red')
    
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