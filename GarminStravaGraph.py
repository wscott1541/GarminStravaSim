#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 09:39:30 2020

@author: WS
"""

import pandas as pd
import matplotlib.pyplot as plt

"""Activities -> All Activities -> Running -> (Sort by most recent first) 
    -> (Scroll down to include all) -> Export -> (Move to correct location)"""
data = pd.read_csv (r'Activities.csv')   
df = pd.DataFrame(data, columns= ['Date','Distance','Time'])

print(df)

dates_times = df['Date'].tolist()
dates = []
for i in range(0,len(dates_times)):
    first_chars = dates_times[i][0:10]
    dates.append(first_chars)
distances = df['Distance'].tolist()
durations = df['Time'].tolist()


sum_distances = []
sum_durations = []
#divmod for durations

def date_string(m,yyyy):
    if m == 10 or m == 11 or m == 12:
        string = '{}-{}'.format(yyyy,m)
    else:
        string = '{}-0{}'.format(yyyy,m)
    return(string)

def duration_sum(m,yyyy):
    sum_distances = [0]
    month_dates = [0]
    
    for i in range(0,len(dates)):
        if date_string(m,yyyy) in dates[i]:
            dist = round(sum_distances[-1] + float(distances[i]),2)
            sum_distances.append(dist)
            month_dates.append(float(dates[i][-2:]))
    #month_dates.append(0)
    #month_dates.reverse()
    #error message?
    return(month_dates,sum_distances)

    
def plot_month_and_previous(m,yyyy):
    curr_month_dates, curr_sum_distances = duration_sum(m,yyyy)
    if m == 1:
        new_year = yyyy - 1 
        prev_month_dates, prev_sum_distances = duration_sum(12,new_year)
    else:
        prev_month_dates, prev_sum_distances = duration_sum((m-1),yyyy)
    
    plt.show()
    plt.plot(prev_month_dates, prev_sum_distances,color='blue')
    print('prev dates: ',prev_month_dates)
    print('prev sum: ',prev_sum_distances)
    plt.plot(curr_month_dates, curr_sum_distances,color='red')
    print('curr dates: ',curr_month_dates)
    print('curr sum: ',curr_sum_distances)
    plt.show()
    
plot_month_and_previous(4,2020)

mar_dates,mar_dist = duration_sum(3,2020)   
print(mar_dates)
print(mar_dist)
"""  
apr_dates,apr_dist = duration_sum(4,2020)
mar_dates,mar_dist = duration_sum(3,2020)

#plt.plot(mar_dates,mar_dist)
plt.plot(apr_dates,apr_dist)
print(apr_dist)
print(apr_dates)  
"""
"""    
month_input = 
mar_twenty_vals = []
apr_twenty_dates = []
apr_distance = [0]
may_twenty_vals = []

for i in range(0,len(dates)):
    if '2020-03' in dates[i]:
        mar_twenty_vals.append(i)
    if '2020-04' in dates[i]:
        apr_twenty_dates.append(dates[i])
        dur = round(apr_distance[-1] + float(distances[i]),2)
        apr_distance.append(dur)
    if '2020-05' in dates[i]:
        may_twenty_vals.append(i)
    
print(apr_twenty_dates)
print(apr_distance)

apr_xs = []
for i in range(0,len(apr_twenty_dates)):
    apr_xs.append(float(apr_twenty_dates[i][-2:]))
apr_xs.append(0)
apr_xs.reverse()    
    
import matplotlib.pyplot as plt

plt.plot(apr_xs,apr_distance)

"""

