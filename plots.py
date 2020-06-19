#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:52:03 2020

@author: WS
"""

from time import time

from datetime import datetime

today = time()

today_dt = datetime.fromtimestamp(today)
today_string = datetime.strftime(today_dt,'%Y-%m-%d')

print(today_string)

year = round(float(datetime.strftime(today_dt,'%Y')))
month = round(float(datetime.strftime(today_dt,'%m')))
day = round(float(datetime.strftime(today_dt,'%d')))

"""
Plot graphs, starting from today
"""

import matplotlib.pyplot as plt
import primary_user_functions as puf#includes importing the data, but not updating


puf.plot_month_distance(month,year,'Running')
plt.show()

puf.plot_month_and_previous_distances(month,year,'Running')
plt.show()
puf.plot_month_and_previous_durations(month,year,'Running')
plt.show()
puf.plot_month_and_previous_distances(month,year,'Cycling')
plt.show()
puf.plot_month_and_previous_distances(month,year,'Walking')
plt.show()

puf.plot_durations_all_previous(month,year,'Running')
plt.show()
puf.plot_distances_all_previous(month,year,'Running')
plt.show()
puf.plot_cumulative_distance(month,year,'Running')
plt.show()

puf.plot_cumulative_distance(month,year,'All')
plt.show()
puf.plot_week_and_previous_distances(today_string,'Running')
plt.show()
puf.plot_week_and_previous_distances(today_string,'Cycling')
plt.show()
puf.plot_week_and_previous_distances(today_string,'All')
plt.show()

import multiple_user_functions as muf

muf.plot_month_distances(month,year,'Running')
plt.show()
muf.plot_distances_this_week(today_string,'Running')
plt.show()
