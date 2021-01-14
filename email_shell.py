#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 17:44:06 2020

@author: WS
"""

import pandas as pd

import email_functions

import data_read as dr

email_data = pd.read_csv (r'email_dates.csv')

dates_df = pd.DataFrame(email_data, columns= ['Email sent'])

dates_list = dates_df['Email sent'].tolist()
latest_date = dates_list[-1]

#import update

from today_string import today_string

if latest_date != today_string:
    
    settings = email_functions.load_settings()
    initials = dr.pull_initials()
    
    email_functions.summary_email(settings,initials)
    
    today = [today_string]
    row = pd.Series(today,index=dates_df.columns)
    new_dates = dates_df.append(row,ignore_index = True)

    new_dates.to_csv(r'email_dates.csv',index = False)