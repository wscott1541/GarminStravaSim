#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:22:17 2020

@author: WS
"""

import matplotlib.pyplot as plt

from today_string import today_string, year, month, day

from datetime import datetime

import data_read as dr

initials = dr.initials_list[0]

dates,distances,durations,types = dr.data_read(initials)

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

def distance_sum(m,yyyy,activity):#can add 'All'
    sum_distances = [0]
    month_dates = [0]
    
    if activity == 'All':
        activity = 'i'
    
    for i in range(0,len(dates)):
        if date_string(m,yyyy) in dates[i] and activity in types[i]:
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

def add_zeros(number):
    if float(number) >= 10:
        string = number
    else:
        string = '0{}'.format(number)
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
        
def duration_sum(m,yyyy,activity):
    plot_mins = [0]
    month_dates = [0]
    
    if activity == 'All':
        activity = 'i'
    
    for i in range(0,len(dates)):
        if date_string(m,yyyy) in dates[i] and activity in types[i]:
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

def plot_month_distance(m,yyyy,activity):
    curr_month_dates, curr_sum_distances = distance_sum(m,yyyy,activity)
    
    title = '{} distances in {} {}'.format(activity,month_caller(m),yyyy)
    
    junk_month_dates,curr_mins = duration_sum(m,yyyy,activity)
    curr_annot = '{} {}: {}km in {} '.format(month_caller(m),yyyy,round(curr_sum_distances[-1]),floatminute_to_stringtime(curr_mins[-1]))
    
    fig,ax = plt.subplots()
    
    plt.plot(curr_month_dates, curr_sum_distances,color='red', label = curr_annot)
    #plt.text(curr_month_dates[-2],curr_sum_distances[-1],curr_annot,horizontalalignment='right')
    ax.legend();
    plt.title(title)
    
def plot_month_and_previous_distances(m,yyyy,activity):
    curr_month_dates, curr_sum_distances = distance_sum(m,yyyy,activity)
    
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
    prev_month_dates, prev_sum_distances = distance_sum(prev_month,new_year,activity)
    
    junk_month_dates,prev_mins = duration_sum(m-1,yyyy,activity)
    prev_annot = '{} {}: {}km in {} '.format(month_caller(m-1),yyyy,round(prev_sum_distances[-1]),floatminute_to_stringtime(prev_mins[-1]))
    
    junk_month_dates,curr_mins = duration_sum(m,yyyy,activity)
    curr_annot = '{} {}: {}km in {} '.format(month_caller(m),yyyy,round(curr_sum_distances[-1]),floatminute_to_stringtime(curr_mins[-1]))
    
    title = '{} distances in {} {} and {} {}'.format(title_activity, month_caller(prev_month),new_year,month_caller(m),yyyy)
    
    fig,ax = plt.subplots()
    plt.plot(prev_month_dates, prev_sum_distances,color='blue',label = prev_annot)
    #plt.text(prev_month_dates[-2],prev_sum_distances[-1],prev_annot,horizontalalignment='right')
    plt.plot(curr_month_dates, curr_sum_distances,color='red', label = curr_annot)
    #plt.text(curr_month_dates[-2],curr_sum_distances[-1],curr_annot,horizontalalignment='right')
    ax.legend();
    plt.title(title)
    
def plot_month_and_previous_durations(m,yyyy,activity):
    
    if activity == 'All':
        activity = 'i'
        title_activity = 'All'
    else:
        title_activity = activity
    
    curr_month_dates, curr_sum_durs = duration_sum(m,yyyy,activity)
    if m == 1:
        new_year = yyyy - 1
        prev_month = 12
    else:
        new_year = yyyy
        prev_month = m - 1
    prev_month_dates, prev_sum_durs = duration_sum(prev_month,new_year,activity)
    
    junk_month_dates,prev_dists = distance_sum(m-1,yyyy,activity)
    prev_annot = '{} {}: {}km in {} '.format(month_caller(m-1),yyyy,round(prev_dists[-1]),floatminute_to_stringtime(prev_sum_durs[-1]))
    
    junk_month_dates,curr_dists = distance_sum(m,yyyy,activity)
    curr_annot = '{} {}: {}km in {} '.format(month_caller(m),yyyy,round(curr_dists[-1]),floatminute_to_stringtime(curr_sum_durs[-1]))
    
    title = '{} durations in {} {} and {} {}'.format(title_activity, month_caller(prev_month),new_year,month_caller(m),yyyy)
    
    fig,ax = plt.subplots()
    plt.plot(prev_month_dates, prev_sum_durs,color='blue',label=prev_annot)
    #plt.text(prev_month_dates[-2],prev_sum_durs[-1],prev_annot,horizontalalignment='right')
    plt.plot(curr_month_dates, curr_sum_durs,color='red',label=curr_annot)
    #plt.text(curr_month_dates[-2],curr_sum_durs[-1],curr_annot,horizontalalignment='right')
    ax.legend();
    plt.title(title)
    
def plot_durations_all_previous(m,yyyy,activity):
    run_vals = []    
    
    title = '{} durations each month'.format(activity)
    
    if activity == 'All':
        activity = 'i'
    
    for i in range(0,len(dates)):
        if activity in types[i]:
            run_vals.append(i)
    val = run_vals[0]
    earliest_date = dates[val]
    
    pick_month = yyyy * 12 + m
    earl_month = datestring_to_floatmonth(earliest_date)
    
    fig,ax = plt.subplots()
    for i in range(earl_month,pick_month+1):
        temp_datestring = floatmonth_to_datestring(i)
        m_val,yyyy_val = pull_month_and_year(temp_datestring)
        temp_dates,temp_sum = duration_sum(m_val,yyyy_val,activity)
        plt.plot(temp_dates,temp_sum,label=temp_datestring)
    if pick_month - earl_month > 6:    
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        ax.legend();
    plt.title(title)
    
def plot_distances_all_previous(m,yyyy,activity):
    run_vals = []    
    
    title = '{} distances each month'.format(activity)
    
    if activity == 'All':
        activity = 'i'
    
    for i in range(0,len(dates)):
        if activity in types[i]:
            run_vals.append(i)
    val = run_vals[0]
    earliest_date = dates[val]
    
    pick_month = yyyy * 12 + m
    earl_month = datestring_to_floatmonth(earliest_date)
    
    fig,ax = plt.subplots()
    for i in range(earl_month,pick_month+1):
        temp_datestring = floatmonth_to_datestring(i)
        m_val,yyyy_val = pull_month_and_year(temp_datestring)
        temp_dates,temp_sum = distance_sum(m_val,yyyy_val,activity)
        plt.plot(temp_dates,temp_sum,label=temp_datestring)
    if pick_month - earl_month > 6:    
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        ax.legend();
    plt.title(title)
    
def plot_distances_this_year(m,yyyy,activity):
    #run_vals = []    
    
    title = '{} distances each month in {}'.format(activity,yyyy)
    
    if activity == 'All':
        activity = 'i'
    
    #for i in range(0,len(dates)):
    #    if activity in types[i]:
    #        run_vals.append(i)
    #val = run_vals[0]
    
    fig,ax = plt.subplots()
    for i in range(1,m+1):
        temp_dates,temp_sum = distance_sum(i,yyyy,activity)
        temp_string = '{} {}: {}km'.format(month_caller(i),yyyy,temp_sum[-1])
        plt.plot(temp_dates,temp_sum,label=temp_string)
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.title(title)
    

    
def plot_cumulative_distance(m,yyyy,activity):
    run_vals = []
    
    title = 'All-time cumulative {} distances'.format(activity)

    if activity == 'All':
        activity = 'i'
    
    for i in range(0,len(dates)):
        if activity in types[i]:
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
        temp_dates,temp_sum = distance_sum(m_val,yyyy_val,activity)
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
    if pick_month - earl_month > 6:    
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        ax.legend();
    plt.title(title)

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

def distance_sum_curr_week(today_string,activity):
    date_strp = datetime.strptime(today_string,'%Y-%m-%d')
    date_object = datetime.timestamp(date_strp)
    
    sum_distances = [0]
    week_dates = [0]
    
    if activity == 'All':
        activity = 'i'#i being, of course, included in the suffix -ing as well as in Cardio
    
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

def distance_sum_prev_week(today_string,activity):
    date_strp = datetime.strptime(today_string,'%Y-%m-%d')
    date_object = datetime.timestamp(date_strp) - 24 * 60 * 60 * 7
    
    sum_distances = [0]
    week_dates = [0]
    
    if activity == 'All':
        activity = 'i'
    
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
  
def plot_week_and_previous_distances(today_string,activity):
   
    title = '{} activities in the two previous weeks'.format(activity)
    
    tw_dates,tw_dist = distance_sum_curr_week(today_string,activity)
    this_annot = 'This week: {}km'.format(tw_dist[-1])
   
    pw_dates,pw_dist = distance_sum_prev_week(today_string,activity)
    prev_annot = 'Last week: {}km'.format(pw_dist[-1])
    
    fig,ax = plt.subplots()
    plt.plot(pw_dates, pw_dist,color='blue',label=prev_annot)
    
    plt.plot(tw_dates, tw_dist,color='red',label=this_annot)
    
    ax.legend(); 
    plt.title(title)
