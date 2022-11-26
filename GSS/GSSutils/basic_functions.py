# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:12:37 2021

@author: WS
"""
###TO HAVE NO REFERENCES TO OTHER MODULES!###

import numpy as np

from datetime import datetime, timedelta
from time import time
from typing import Optional

from . import today_string as ts

def time_check():
    today = time()
    today_dt = datetime.fromtimestamp(today)
    time_string = datetime.strftime(today_dt,'%H:%M:%S.%f')
    print(time_string)

def floatmonth_to_datestring(floatmonth):
    new = divmod(floatmonth,12)
    new_year = new[0]
    new_month = new[1]
    if new_month == 0:
        new_year = new_year - 1
        new_month = 12
    string = date_string(new_month,new_year)
    return(string)

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

def month_length(m: float, yyyy: float, d:Optional[float]=None)->float:#sighhh
    
    if m in (1, 3, 5, 7, 8, 10, 12):
        length = 31
    elif m in (4, 6, 9, 11):
        length = 30    
    elif m == 2 and yyyy in (2016, 2020, 2024):
        length = 29
    elif m == 2:
        length = 28
        
    if m == ts.month and yyyy == ts.year:#i.e. is the current month of the year 
        length = ts.day
    
    if d:#unless we've said we'd like a different month 
        length = d
    
    return length

def add_zeros(str_n):
    if float(str_n) >= 10 or float(str_n) == 0:
        string = str(str_n)
    else:
        string = '0{}'.format(str_n)
        
    if string == '0':
        string = '00'
    
    
    return(string)

def time_string(n):
    if n < 10:
        string = '0{}'.format(round(n))
    else:
        string = '{}'.format(round(n))
    return(string)

def stringtime_to_floatminute(time_string):
        hours = float(time_string[:2])
        minutes = float(time_string[3:5])
        seconds = float(time_string[6:8])
    
        time = hours * 60 + minutes + seconds/60
    
        return(time)

def floatminute_to_stringtime(time):
    hours_calc = list(divmod(time,60))
    hours = hours_calc[0]
    remaining = hours_calc[1]
    mins_calc = list(divmod(remaining,1))
    minutes = mins_calc[0]
    seconds = mins_calc[1]
    
    if round(seconds*60) == 60:
        minutes = minutes + 1
        seconds = 0
    
    hour_string = time_string(hours)
    mins_string = time_string(minutes)
    secs_string = time_string(round(seconds * 60)) 
    
    string = '{}:{}:{}'.format(hour_string,mins_string,secs_string)
    
    #if time == 0:
    #    string = '00:00:00'
    
    return(string)

def cropped_floatminute_to_stringtime(time):
    
    string = floatminute_to_stringtime(time)
    
    if '00' in string[:2]:
        string = string[3:]
        
    if string[0] == '0':
        string = string[1:]
    
    return(string)
    

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

def minutes_axes_label(minutes):
    final = minutes[-1]
    
    #print(final)
    
    if final > 300:
        tags,points = minutes_loop(final,60)
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

def convert_time(x):
    if str(type(x))  == "<class 'str'>":
        x = datetime.strptime(x,'%Y-%m-%d %H:%M:%S')
    return(x)


def durl_to_dtag(durl):
    
    mappings = {
        '1mile': '1 mile',
        '1.5mile': '1.5 mile',
        '3mile': '3 mile',
        '5mile': '5 mile',
        '10mile': '10 mile'
                }

    if durl in mappings:
        dtag = mappings[durl]
    else:
        dtag = durl

    return(dtag)

def dtag_to_durl(dtag):
    
    mappings = {
        '1 mile': '1mile',
        '1.5 mile': '1.5mile',
        '3 mile': '3mile',
        '5 mile': '5mile',
        '10 mile': '10mile'
                }

    if dtag in mappings:
        durl = mappings[dtag]
    else:
        durl = dtag

    return(durl)

def running_filter(df):
    
    df = df.loc[df['Activity Type'] == 'Running']
    
    return(df)

def split_to_dt(x):
    
    x = datetime.strptime(str(x)[-8:], '%H:%M:%S')# - datetime.strptime("00:00:00", "%H:%M:%S")
    
    return(x)

def split_to_floatminute(x):
    
    x = str(x)[-8:]
    
    x = stringtime_to_floatminute(x)
    
    return(x)

def seconds_to_str_minutes(x: float):
    #ty_res = time.gmtime(x)
    #res = time.strftime("%H:%M:%S",ty_res).lstrip('0:')
    #raise ValueError(x, type(x))
    
    minus = '-' if x < 0 else ''
    res = str(timedelta(seconds = abs(x)))
    
    if res[:2] == '0:':
        res = res[2:]

    return minus+res

def isnan(x)->bool:
    if isinstance(x, (float, int)):
        return np.isnan
    else:
        return True
        

    
