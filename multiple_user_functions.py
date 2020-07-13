#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:43:40 2020

@author: WS
"""

import matplotlib.pyplot as plt

from time import time#, localtime
from datetime import datetime

today = time()

today_dt = datetime.fromtimestamp(today)

today_string = datetime.strftime(today_dt,'%Y-%m-%d')
"""
now = list(localtime(today))
year = now[0]
month = now[1]
day = now[2]
"""
year = round(float(datetime.strftime(today_dt,'%Y')))
month = round(float(datetime.strftime(today_dt,'%m')))
day = round(float(datetime.strftime(today_dt,'%d')))
###it'd be nice if I could get it all to work with datetime strings tbh

import data_read as dr

from primary_user_functions import month_length, date_string, populate_arrays_generic

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

def distance_sum(m,yyyy,activity,initials):#can add 'All'
    sum_distances = [0]
    month_dates = [0]
    
    if activity == 'All':
        activity = 'i'
    
    dates,distances,durations,types = dr.data_read(initials)
    
    for i in range(0,len(dates)):
        if date_string(m,yyyy) in dates[i] and activity in types[i]:
            dist = round(sum_distances[-1] + float(distances[i]),2)
            sum_distances.append(dist)
            month_dates.append(float(dates[i][-2:]))
    
    populate_arrays(m,yyyy,month_dates,sum_distances)
    
    #error message?
    return(month_dates,sum_distances)
    
def plot_month_distances(m,yyyy,activity):
    
    title = '{} activities this month'.format(activity)
    
    if activity == 'All':
        activity = 'i'#i being, of course, included in the suffix -ing as well as in Cardio
    
    fig,ax = plt.subplots()
    for n in range(0,len(dr.initials_list)):
        
        month_dates, sum_distances = distance_sum(m,yyyy,activity,dr.initials_list[n])
        annot = '{}: {}km'.format(dr.initials_list[n],sum_distances[-1])
        
        plt.plot(month_dates, sum_distances,label = annot)
        
    ax.legend();
    
    plt.title(title)
    
def distance_sum_week(today_string,activity,initials):
    date_strp = datetime.strptime(today_string,'%Y-%m-%d')
    date_object = datetime.timestamp(date_strp)
    
    sum_distances = [0]
    week_dates = [0]
    
    if activity == 'All':
        activity = 'i'#i being, of course, included in the suffix -ing as well as in Cardio
        
    dates,distances,durations,types = dr.data_read(initials)
        
    for i in range(1,8):
        temp_date_object = date_object - (24 * 60 * 60) * ((7-i))
        temp_date_dt = datetime.fromtimestamp(temp_date_object)
        temp_date_string = datetime.strftime(temp_date_dt,'%Y-%m-%d')
        
        for d in range (0,len(dates)):
            if temp_date_string in dates[d] and activity in types[d]:
                dist = round(sum_distances[-1] + float(distances[d]),2)
                sum_distances.append(dist)
                week_dates.append(i)
   
    populate_arrays_generic(7,week_dates,sum_distances)
    
    if week_dates[1] == 0:
        sum_distances.remove(sum_distances[0])
        week_dates.remove(week_dates[0])
    
    #error message?
    return(week_dates,sum_distances)
  
def plot_distances_this_week(today_string,activity):
   
    title = '{} activities this week'.format(activity)
    
    fig,ax = plt.subplots()
    for n in range(0,len(dr.initials_list)):
        
        month_dates, sum_distances = distance_sum_week(today_string,activity,dr.initials_list[n])
        annot = '{}: {}km'.format(dr.initials_list[n],sum_distances[-1])
        
        plt.plot(month_dates, sum_distances,label = annot)
        
    ax.legend();
   
    plt.title(title)
    

    