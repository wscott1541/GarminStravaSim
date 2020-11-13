#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:22:17 2020

@author: WS
"""

import matplotlib.pyplot as plt

from today_string import today_string, year, month, day, y_day_string

from datetime import datetime, timedelta

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

def add_zeros(str_n):
    if float(str_n) >= 10 or float(str_n) == 0:
        string = str_n
    else:
        string = '0{}'.format(str_n)
    
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
    secs_string = time_string(round(seconds * 60))
    
    string = '{}:{}:{}'.format(hour_string,mins_string,secs_string)
    
    #if time == 0:
    #    string = '00:00:00'
    
    return(string)
    
def stringtime_to_floatminute(time_string):
        hours = float(time_string[:2])
        minutes = float(time_string[3:5])
        seconds = float(time_string[6:8])
    
        time = hours * 60 + minutes + seconds/60
    
        return(time)

def minutes_crop(string):
    if string[:2] == '00':
        new = string[3:]
    else:
        new = string
    
    return(new)

def minutes_loop(final,multiple):
    
    tags = [0]
    points = [0]
    
    val = multiple
    
    while val < final:
        
        tag = floatminute_to_stringtime(val)
        
        tag = minutes_crop(tag)
        
        tags.append(tag)
        points.append(val)
        
        val += multiple
        
    final_tag = floatminute_to_stringtime(final)
    final_tag = minutes_crop(final_tag)
    
    tags.append(final_tag)
    points.append(final)
    
    return(tags,points)
    
#t,p = minutes_loop(48,5)
#print(t,p)

    
def minutes_axes_label(minutes):
    final = minutes[-1]
    
    if final > 300:
        tags,poitns = minutes_loop(final,60)
    elif final > 180:
        tags,points = minutes_loop(final,45)
    elif final > 90:
        tags,points = minutes_loop(final,15)
    elif final > 60:
        tags,points = minutes_loop(final,10)
    elif final > 30:
        tags,points = minutes_loop(final,5)
    else:
        tags,points = minutes_loop(final,3)
        
    return(tags,points)

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
    
def daily_rolling_average(today_string,activity):
    dists = []
    
    day_obj = datetime.strptime(today_string,'%Y-%m-%d')
    earl = day_obj - timedelta(days=30)
    
    if activity == 'All':
        activity = 'i'
    
    for i in range(0,len(dates)):
        date_stamp = dates[i][:10]
        date_obj = datetime.strptime(date_stamp,'%Y-%m-%d')
        
        if date_obj > earl and date_obj < day_obj and activity in types[i]:
            dists.append(distances[i])
            
    daily_average = round(sum(dists)/28,2)
    
    return(daily_average)
    
def weekly_rolling_average(today_string,activity):
    daily_average = daily_rolling_average(today_string,activity)
    weekly_average = round(7 * daily_average,2)
    
    return(weekly_average)

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
        if i < 11:
            plt.plot(temp_dates,temp_sum,label=temp_string)
        elif i == 11:
            plt.plot(temp_dates,temp_sum,label=temp_string,color='deeppink')
        elif i == 12:
            plt.plot(temp_dates,temp_sum,label=temp_string,color='lime')
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.title(title)
    
#plot_distances_this_year(12,2019,'Running')
    
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
    
    ax.set_ylabel('Distance (km)')
    
    x_labels = []
    i = 0
    while i < 7:
        day = datetime.strptime(today_string,'%Y-%m-%d') - timedelta(days=(7+i))
        tag = datetime.strftime(day,'%a')
        x_labels.append(tag)
        i += 1
    
    x_labels.reverse()
    #0.5,1.5,2.5,3.5,4.5,5.5,6.5
    ax.set_xticks([1,2,3,4,5,6,7])
    ax.set_xticklabels(x_labels)
    
    ax.legend(); 
    plt.title(title)
    
#ac_df = dr.pull_data('WS')
#days,vals = week_duration_sum_list(ac_df,today_string,'Cardio')
#plot_week_and_previous_distances(today_string,'Running')

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

def week_duration_sum_list(activities_df,date_string,activity):
    dur_strings = activities_df['Time'].tolist()
    dates = activities_df['Date'].tolist()
    types = activities_df['Activity Type'].tolist()
    
    durs = []
    
    for i in range(0,len(dur_strings)):
        dur = stringtime_to_floatminute(dur_strings[i])
        
        durs.append(dur)
    
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
        date_obj = datetime.strptime(dates[i],'%Y-%m-%d %H:%M:%S')
        date_str = datetime.strftime(date_obj,'%Y-%m-%d')
        date_obj = datetime.strptime(date_str,'%Y-%m-%d')
        
        if date_obj >= sta_date and date_obj <= end_date and activity in types[i]:
            if len(vals) > 0:
                dur_sum = vals[-1] + durs[i]
            else:
                dur_sum = durs[i]
            
            vals.append(dur_sum)
            
            day_string = datetime.strftime(date_obj,'%Y-%m-%d')
            day_strf = datetime.strptime(day_string,'%Y-%m-%d')
            
            days.append(day_strf)
    
    populate_list(sta_date,end_date,days,vals)
    
    #print(days)
    #print(vals)
    
    return(days, vals)
    
#ac_df = dr.pull_data('WS')
#d,v = week_duration_sum_list(ac_df,today_string,'Running')

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

#print(d)
    
#order_date_vals(d)    
    
def plot_week_previous_durations(activities_df,date_string,activity):
    
    title = '{} activities in the two previous weeks'.format(activity)
    
    if activity == 'All':
        activity = 'i'
    
    curr_week = datetime.strptime(date_string,'%Y-%m-%d')
    prev_week = curr_week - timedelta(days=7)
    #print(prev_week)
    prev_string = datetime.strftime(prev_week,'%Y-%m-%d')
    
    curr_days,curr_vals = week_duration_sum_list(activities_df,date_string,activity)
    curr_days = order_date_vals(curr_days)
    curr_annot = 'This week: {}'.format(floatminute_to_stringtime(curr_vals[-1]))
    prev_days,prev_vals = week_duration_sum_list(activities_df,prev_string,activity)
    prev_days = order_date_vals(prev_days)
    prev_annot = 'Last week: {}'.format(floatminute_to_stringtime(prev_vals[-1]))
    
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
    
    if prev_vals[-1] > curr_vals[-1]:
        highest = prev_vals
    else:
        highest = curr_vals
        
    y_tags,y_ticks = minutes_axes_label(highest)
    
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_tags)
    
    ax.set_ylabel('Duration')
    
    ax.legend(); 
    plt.title(title)    
    
#ac_df = dr.pull_data('WS')
#days,vals = week_duration_sum_list(ac_df,today_string,'Cardio')
#plot_week_previous_durations(ac_df,today_string,'Running')
    
"""
def plot_week_and_previous_distances(activities_df,date_string,activity):
   
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
"""        

def furthest(category):
    running_dates = []
    running_dists = []
    
    for i in range(0,len(dates)):
        if category in types[i]:
            
            if len(running_dists) == 0 or distances[i] > running_dists[-1]:
                running_dists.append(distances[i])
                running_dates.append(dates[i])
        
    if len(running_dists) > 0:
        dist = running_dists[-1]
        date = running_dates[-1]
        
        out = 'Furthest: {}km on {}'.format(dist,date[:10])
    else:
        out = 'NONE'
        
    return(out)

import analyse

def personal_best(category):
    full_types,full_dates,full_dists,full_splits = dr.all_times(initials,category)
    
    running_dates = []
    running_splits = []
    
    for i in range(0,len(full_splits)):
        if full_splits[i] != 'NONE':
            if len(running_splits) == 0 or full_splits[i] < running_splits[-1]:
                running_splits.append(full_splits[i])
                running_dates.append(full_dates[i])
        
    if len(running_splits) > 0:
        best_time = running_splits[-1]
        best = analyse.best_time_string(best_time)
        date = running_dates[-1]
        
        best = best + ' on {}'.format(date[:10])
    else:
        best = 'NONE'
        
    if 'C' in category:
        category = category[1:]
        
    if category == 'Half':
        category = 'Half marathon'
    if category == 'Full':
        category = 'Marathon'
    
    string = '{}: {}'.format(category,best)
    
    return(string)   

#column reference: ['Activity number','Activity Type','Date','Distance','Time','1km','1 mile','1.5 mile','3 mile','5km','10km','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Status']
    
def all_personal_bests():
    body = f"""
{personal_best('1km')}
{personal_best('1 mile')}
{personal_best('1.5 mile')}
{personal_best('3 mile')}
{personal_best('5km')}
{personal_best('10km')}
{personal_best('20km')}
{personal_best('Half')}
{personal_best('Full')}
{furthest('Running')}
{personal_best('C10k')}
{personal_best('C20k')}
{personal_best('C50k')}
{personal_best('C100k')}
{personal_best('C200k')}
{personal_best('C250k')}
{furthest('Cycling')}
"""
    
    return(body)
    
def all_personal_bests_html():

    html = f"""\
<body>
    <p><b><u>Personal bests</u></b><br>
    <b>Running</b><br>
    {personal_best('1km')}<br>
    {personal_best('1 mile')}<br>
    {personal_best('1.5 mile')}<br>
    {personal_best('3 mile')}<br>
    {personal_best('5km')}<br>
    {personal_best('10km')}<br>
    {personal_best('20km')}<br>
    {personal_best('Half')}<br>
    {personal_best('Full')}<br>
    {furthest('Running')}<br>
    <b>Cycling</b><br>
    {personal_best('C10k')}<br>
    {personal_best('C20k')}<br>
    {personal_best('C50k')}<br>
    {personal_best('C100k')}<br>
    {personal_best('C200k')}<br>
    {personal_best('C250k')}<br>
    {furthest('Cycling')}</p>
  </body>
"""

    return(html)

"""
NOTE: values  start to be redefined from this 
"""
week_types,week_dates,week_dists,dummy_splits = dr.week_times(initials,'1km')

def activity_check():
    
    week_events = len(week_types)
    running_events_sub = []
    cycling_events_sub = []
    walking_events_sub = []
    other_events_sub = []
        
    if week_events != 0:
        for i in range(0,week_events):
            if week_types[i] == 'Running':
                running_events_sub.append(1)
            elif week_types[i] == 'Cycling':
                cycling_events_sub.append(1)
            elif week_types[i] == 'Walking' or week_types[i] == 'Hiking':
                walking_events_sub.append(1)
            else:
                other_events_sub.append(1)
    
    running_events = len(running_events_sub)
    cycling_events = len(cycling_events_sub)
    walking_events = len(walking_events_sub)
    other_events = len(other_events_sub)
    
    return(week_events,running_events,cycling_events,walking_events,other_events)
    
#week_events,running_events,cycling_events,walking_events,other_events = activity_check(

def week_best(category):
    full_types,full_dates,full_dists,full_splits = dr.week_times(initials,category)
    
    running_dates = []
    running_splits = []
    
    for i in range(0,len(full_splits)):
        if full_splits[i] != 'NONE':
            if len(running_splits) == 0 or full_splits[i] < running_splits[-1]:
                running_splits.append(full_splits[i])
                running_dates.append(full_dates[i])
        
    if len(running_splits) > 0:
        best_time = running_splits[-1]
        best = analyse.best_time_string(best_time)
        date = running_dates[-1]
        
        best = best + ' on {}'.format(date[:10])
    else:
        best = 'NONE'
    
    string = '{}: {}'.format(category,best)
    
    return(string)


def activity_week_summary_html(activity_type):
    week_events,running_events,cycling_events,walking_events,other_events = activity_check()
    
    event_dates,distance_sum = distance_sum_curr_week(y_day_string,activity_type)
    total_distance = distance_sum[-1]

    if activity_type == 'Running':
        verb = 'ran'
        event = 'runs'
        n_events = running_events
    if activity_type == 'Cycling':
        verb = 'cycled'
        event = 'rides'
        n_events = cycling_events
    if 'king' in activity_type:
        verb = 'walked or hiked'
        event = 'walks or hikes'
        n_events = walking_events
    #else:
    #    verb = 'did?'    
    #    event = 'events?'
    
    summary = f"""<p><b>{activity_type}</b><br><p>
<p>You {verb} <b>{total_distance}km</b> across {n_events} {event}, against a weekly average of {weekly_rolling_average(today_string,activity_type)}km.<p>"""
    
    if activity_type == 'Running':
        bests = f"""<p>              
{week_best('1km')}<br>
{week_best('1 mile')}<br>
{week_best('1.5 mile')}<br>
{week_best('3 mile')}<br>
{week_best('5km')}<br>
{week_best('10km')}<br>
{week_best('20km')}<br>
{week_best('Half')}<br>
{week_best('Full')}</p>
 """
        summary = summary + bests
    if activity_type == 'Cycling':
        bests = f"""<p>              
{week_best('C10k')}<br>
{week_best('C20k')}<br>
{week_best('C50k')}<br>
{week_best('C100k')}<br>
{week_best('C200k')}<br>
{week_best('C250k')}</p>
 """
        summary = summary + bests
    
    return(summary)

def simple_week_update_html(start_date):
    
    earliest_date = datetime.strptime(start_date,'%Y-%m-%d') - timedelta(days=7)
    
    e_d_strip = datetime.strftime(earliest_date,'%Y-%m-%d')
    
    opening = f"""
<p><u><b>Activities from {e_d_strip} to {start_date}</b></u></p>"""   

    for i in range(0,len(dates)):
        
        date_obj = datetime.strptime(dates[i],'%Y-%m-%d')
        
        if date_obj > earliest_date:
            
            activity_text = f"""
<p><u>{types[i]}, {dates[i]}</u>: {distances[i]}km in {durations[i]} minutes.</p>
"""
            
            opening = opening + activity_text
            
    body = f"""
<body>
{opening}
</body>"""

    return(body)
        
def week_summary_html(start_date):
    week_events,running_events,cycling_events,walking_events,other_events = activity_check()
    
    if week_events == 0:
        body = f"""
<body>
<p>Your last activity was on {dates[-1]}.<p>
</body> 
        """
    else:
        body = """
<body>
<p><b><u>This week:</u></b></p>
</body>
"""
        #chunks = [opening]
        if running_events > 0:
            chunk = f"""
<body>
{activity_week_summary_html('Running')}
</body>
"""
            #chunks.append(chunk)
            body = body + chunk
        if cycling_events > 0:
            chunk = f"""
<body>
{activity_week_summary_html('Cycling')}
</body>
"""
            #chunks.append(chunk)
            body = body + chunk
            #chunks.append(chunk)
        
        #body = chunks[0]
        
        if walking_events > 0:
            chunk = f"""
<body>
{activity_week_summary_html('Walking')}
</body>
"""
            #chunks.append(chunk)
            body = body + chunk
        
        #for n in range(1,len(chunks)):
        #    body =+ chunks[n]
        
        if other_events > 0:
            earliest_date = datetime.strptime(start_date,'%Y-%m-%d') - timedelta(days=7)
            
            chunk = """<p><b>Misc. activities</b><br>"""
            
            for i in range(0,len(dates)):
        
                date_obj = datetime.strptime(dates[i],'%Y-%m-%d')
        
                if date_obj > earliest_date:
                    
                    if types[i] == 'Cardio':
                        sub_chunk = f"""
<u>{types[i]}</u>, {dates[i]}: {floatminute_to_stringtime(durations[i])}.<br>
"""
                        chunk = chunk + sub_chunk
                    else:
                        sub_chunk = f"""
<u>{types[i]}</u>, {dates[i]}: {distances[i]}km in {floatminute_to_stringtime(durations[i])}.<br>
"""
                        chunk = chunk + sub_chunk
                        
            chunk = f"""
<body>{chunk[:-5]}</p></body>"""

            body = body + chunk
    
    html = f"""
{body}
"""
    
    return(html)
    
#print(week_summary_html(y_day_string))   
    
def html_assessment(user_df,ac_number):    
    
    ac_type = dr.activity_details(user_df,ac_number,'Type')
    date = dr.activity_details(user_df,ac_number,'Date')
    dist = dr.activity_details(user_df,ac_number,'Distance')
    dur = dr.activity_details(user_df,ac_number,'Duration')
    
    noun,verb,plural = analyse.words(ac_type)
    
    all_dists = []
    all_durs = []
    
    abbr_date = date[:10]
    date_strp = datetime.strptime(abbr_date,'%Y-%m-%d')
    date_obj = datetime.timestamp(date_strp)
    
    for i in range(0,len(dates)):
        temp_d_strp = datetime.strptime(dates[i],'%Y-%m-%d')
        temp_d_obj = datetime.timestamp(temp_d_strp)
        
        if ac_type == types[i] and temp_d_obj < date_obj:
            
            all_dists.append(distances[i])
            all_durs.append(durations[i])
    try:        
        avg = round(sum(all_dists)/len(all_dists),2)
    except:
        avg = 0
    
    full = len(all_durs) + 1
    
    if ac_type != 'Cardio':
        opening = f"""
<body><p>At {date[11:]} on {date[:10]}, you {verb} <b>{dist}km</b> in <b>{dur}</b>, a pace of {analyse.pace(user_df,ac_number)}/km.<br>
This was {noun} {full}, and compared to an average of {avg}km.<br>
This was your {full + 1 - dr.split_rank(user_df,ac_number,'Distance')} furthest and {full + 1 - dr.split_rank(user_df,ac_number,'Time')} longest {noun}.<br>
{shoes_distance_html(user_df,ac_number)}</p></body>
"""
    else:
        opening = f"""
<body>
<p>You worked out for {dur} on {date[:10]} at {date[11:]}.</p></body>
"""
    
    if ac_type == 'Running':
        part = f"""{html_activity_lines(user_df, ac_number)}"""
        statement = opening + part
    else:
        statement = opening
        
    return(statement)

def fastest_since(user_df,activity_number,distance):
    
    split = dr.activity_splits(user_df,activity_number,distance)
    
    #ac_numbers = user_df['Activity number'].tolist()
    dates = user_df['Date'].tolist()
    splits = user_df[distance].tolist()
    
    dates.reverse()
    splits.reverse()
    
    found = False
    cont = True
    slowest = True
    
    date = []
    
    while cont == True:
        for i in range(0,len(splits)):
            if splits[i] != 'NONE':
                if splits[i] > split and slowest == True:
                    slowest = False
                if splits[i] < split:
                    date.append(dates[i])
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
        out = f'fastest since {date[0][:10]}'
    
    return(out)
        
    #return(n)

def greatest_rank(user_df,activity_number,dist_dur):
    ac_type = dr.activity_details(user_df,activity_number,'Type')
    
    rank = dr.split_rank(user_df,activity_number,dist_dur)
    
    #print(rank)
    
    full = user_df['Activity Type'].tolist()
    
    same = 0
    
    for i in range(0,len(full)):
        if ac_type == full[i]:
            same += 1
    
    new_rank = same + 1 - rank
    
    text = f'{new_rank}/{same}'
    
    return(text)

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
    
    found = False
    cont = True
    
    date = []
    
    for i in range(0,len(splits)):
        #print(ac_type,types[i],splits[i],split,cont)
        if ac_type == types[i] and splits[i] > split and cont == True:
            date.append(dates[i])
            cont = False
            found = True
    
    if found == False:
        if 'Time' in dist_dur:
            out = 'longest!'
        if 'Dist' in dist_dur:
            out = 'furthest!'
    else:
        if 'Time' in dist_dur:
            out = f'longest since {date[0][:10]}'
        if 'Dist' in dist_dur:
            out = f'furthest since {date[0][:10]}'
    
    return(out)


#AB5G2247.FIT

#ws_df = dr.pull_data('WS')
#print('Pulled')
#print(fastest_since(ws_df,'AB5G2247','1.5 mile'))

def html_activity_line(distance, user_df, ac_number):
    
    if distance == 'Half':
        text = 'Half marathon'
    elif distance == 'Full':
        text = 'Marathon'
    else:
        text = distance
    
    line = f"<b>{text}</b>: {str(dr.activity_splits(user_df,ac_number,distance))[-8:]} - {dr.split_rank(user_df,ac_number,distance)}/{dr.split_count(user_df,distance)} - {fastest_since(user_df,ac_number,distance)}"
    
    return(line)

#ac_no = dr.latest_activity('WS')
#ws_df = dr.pull_data('WS')
#print(html_activity_line('1km',ws_df,ac_no))    


def html_activity_lines(user_df, ac_number):
    
    text = f"{html_activity_line('1km', user_df, ac_number)}"
    
    options = ['1 mile', '1.5 mile', '3 mile', '5km', '10km', '20km', 'Half', 'Full']
    
    for i in range(0,len(options)):
        
        sec = f"""<br>
{html_activity_line(options[i], user_df, ac_number)}"""
    
        if 'NONE' not in sec:
            text = text + sec
         
    text = text + f"""<br>
<b>Distance</b>: {dr.activity_details(user_df,ac_number,'Distance')}km - {greatest_rank(user_df,ac_number,'Distance')} - {greatest_since(user_df,ac_number,'Distance')}<br>
<b>Duration</b>: {dr.activity_details(user_df,ac_number,'Time')} - {greatest_rank(user_df,ac_number,'Time')} - {greatest_since(user_df,ac_number,'Time')}""" 
            
    full = f"""<body><p>
{text}
</p></body>"""

    return(full)

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
    
    title = '{} distances in {}'.format(activity,month_caller(m))
    
    if activity == 'All':
        activity = 'i'
    
    for i in range(0,len(dates)):
        if activity in types[i] and f'-{add_zeros(m)}-' in dates[i]:
            run_vals.append(i)
    val = run_vals[0]
    earliest_date = dates[val]
    earliest_year = int(earliest_date[:4])
    
    #pick_month = yyyy * 12 + m
    #earl_month = datestring_to_floatmonth(earliest_date)
    
    fig,ax = plt.subplots()
    for y in range(earliest_year,yyyy+1):
        temp_dates,temp_sum = distance_sum(m,y,activity)
        temp_label = f'{y}: {temp_sum[-1]}km'
        plt.plot(temp_dates,temp_sum,label=temp_label)
    
    if yyyy+1 - 2016 > 6:    
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        ax.legend();
    
    plt.title(title)
    
def activity_comparisons(user_df,activity_number):
    ac_type = dr.activity_details(user_df,activity_number,'Type')
    dist = dr.activity_details(user_df,activity_number,'Distance')
    dur = dr.activity_details(user_df,activity_number,'Duration')
    dur = stringtime_to_floatminute(dur)
    
    ac_nos = user_df['Activity number'].tolist()
    ac_types = user_df['Activity Type'].tolist()
    dists = user_df['Distance'].tolist()
    durs = user_df['Time'].tolist()
    
    for i in range(0,len(ac_nos)):
        if ac_types[i] == ac_type and ac_nos[i] != activity_number and dists[i]<25:
            i_dur = stringtime_to_floatminute(durs[i])
            plt.scatter(dists[i],i_dur,color='blue')
            
    plt.scatter(dist,dur,color='red')
    
    plt.xlabel("Distance (km)")
    plt.ylabel('Duration (mins)')
    
def shoes_distance(user_df,pair_of_shoes):
    
    shoes = user_df['Shoes'].tolist()  
    dists = user_df['Distance'].tolist()    
    
    shoe_dists = []
    
    for i in range(0,len(shoes)):
        if pair_of_shoes == shoes[i]:
            shoe_dists.append(dists[i])
            
    shoe_distance = round(sum(shoe_dists),1)
    
    return(shoe_distance)
    
def shoes_distance_html(user_df,activity_number):
    
    shoes = dr.activity_details(user_df,activity_number,'Shoes')
    
    dist = shoes_distance(user_df,shoes)
    
    if dist > 1000:
        dist_html = f'<b><u>{dist}!!!</u></b>'
    elif dist > 800:
        dist_html = f'<b><u>{dist}!</u></b>'
    elif dist > 600:
        dist_html = f'<b><u>{dist}</u></b>'
    elif dist > 400:
        dist_html = f'<u>{dist}</u>'
    else:
        dist_html = f'{dist}'
    
    html = f"""{shoes}: {dist_html}km"""
    
    return(html)


        
    

#ws_df = dr.pull_data('WS')  
#print(shoes_distance_html(ws_df,'4854330057'))


#activity_comparisons(ws_df,'AB3G1638')
#plot_distances_equiv_month(ws_df,10,2020,'All')
    
    
    
