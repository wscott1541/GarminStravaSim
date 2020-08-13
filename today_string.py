#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 17:10:24 2020

@author: WS
"""

"""
https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
"""

from time import time#, localtime
from datetime import datetime, timedelta

today = time()

today_dt = datetime.fromtimestamp(today)

today_string = datetime.strftime(today_dt,'%Y-%m-%d')

time_string = datetime.strftime(today_dt,'%H:%M:%S')

y_day_dt = today_dt - timedelta(days=1)

y_day_string = datetime.strftime(y_day_dt,'%Y-%m-%d')

"""
now = list(localtime(today))
year = now[0]
month = now[1]
day = now[2]
"""
year = round(float(datetime.strftime(today_dt,'%Y')))
month = round(float(datetime.strftime(today_dt,'%m')))
day = round(float(datetime.strftime(today_dt,'%d')))

"""
row_date_strp = datetime.strptime(row_date_string,'%Y-%m-%d %H:%M:%S')
        row_date_object = datetime.timestamp(row_date_strp)
"""