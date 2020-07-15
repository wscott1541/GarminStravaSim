#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:23:16 2020

@author: WS
"""

import time

#sort activity into vaguely useable forms
def pull_from_activity(activity):
    string_activity = str(activity)

    string_activity = string_activity.replace('[{','')
    string_activity = string_activity.replace('}]','')

    list_activity_strings = string_activity.split(',')

    #pull useful information (date, type, duration, distance)
    number_string = list_activity_strings[0][14:]
    date_string = list_activity_strings[3][20:-1]
    type_string = list_activity_strings[6][13:-1]    
    type_string = type_string.capitalize()
    if type_string == 'Indoor_cardio':
        type_string = 'Cardio'
    durs_string = list_activity_strings[16][20:]#16 is elapsed duration (ms), 15 is duration (s)
    dist_string = list_activity_strings[14][13:]
    dist_float = round(float(dist_string)/1000,2)#convert from m to km
    dist_string = str(dist_float)

    durs_float = float(durs_string)/1000#convert from milliseconds to seconds
    durs_string = time.strftime('%H:%M:%S',time.gmtime(durs_float))

    row = [number_string,type_string,date_string,dist_string,durs_string]
    
    return(row)

