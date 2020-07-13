#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:52:03 2020

@author: WS
"""

from today_string import today_string, year, month

"""
Plot graphs, starting from today
"""
#import matplotlib.pyplot as plt
import primary_user_functions as puf#includes importing the data, but not updating
import multiple_user_functions as muf

"""List plots"""

puf.plot_month_distance(month,year,'Running')

puf.plot_month_and_previous_distances(month,year,'Running')

puf.plot_month_and_previous_durations(month,year,'Running')

puf.plot_month_and_previous_distances(month,year,'Cycling')

puf.plot_month_and_previous_distances(month,year,'Walking')

puf.plot_durations_all_previous(month,year,'Running')

puf.plot_distances_all_previous(month,year,'Running')

puf.plot_distances_this_year(month,year,'Running')

puf.plot_cumulative_distance(month,year,'Running')

puf.plot_cumulative_distance(month,year,'All')

puf.plot_week_and_previous_distances(today_string,'Running')

puf.plot_week_and_previous_distances(today_string,'Cycling')

puf.plot_week_and_previous_distances(today_string,'All')

muf.plot_month_distances(month,year,'Running')

muf.plot_distances_this_week(today_string,'Running')

