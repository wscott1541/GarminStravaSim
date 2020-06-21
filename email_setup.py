#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 16:51:38 2020

@author: WS
"""

smtp_server = input('stmp server: ')
port = input('Port: ')
sender_email = input('Email: ')
password = input('Password: ')

import pandas as pd

titles = pd.DataFrame(columns= ['smtp server','Port','Email','Password'])

details = [smtp_server,port,sender_email,password]
row = pd.Series(details,index=titles.columns)
email_settings = titles.append(row,ignore_index = True)

email_settings.to_csv(r'email_settings.csv',index = False)

from today_string import y_day_string

dates_init = pd.DataFrame(columns= ['Email sent'])
yesterday = [y_day_string]
row = pd.Series(yesterday,index=dates_init.columns)
dates = dates_init.append(row,ignore_index = True)

dates.to_csv(r'email_dates.csv',index = False)