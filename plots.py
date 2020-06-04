#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 09:11:00 2020

@author: WS
"""

from time import time, ctime, localtime

t = time()
print_time = ctime(t)
print(print_time)

now = list(localtime(t))
year = now[0]
month = now[1]
day = now[2]

"""
Plot graphs, starting from today
"""

import matplotlib.pyplot as plt
import functions as func#includes importing the data, but not updating

func.plot_month_and_previous_distances(month,year)
plt.show()
func.plot_month_and_previous_durations(month,year)
plt.show()
func.plot_durations_all_previous(month,year)
plt.show()
func.plot_distances_all_previous(month,year)
plt.show()
func.plot_cumulative_distance(month,year)
plt.show()
