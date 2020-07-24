#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 17:09:14 2020

@author: WS
"""

import pandas as pd

from fitparse import FitFile

#work out way of importing
fitfile = FitFile('A7NH3442.FIT')

timestamps = []
#note that this is possibly not GMT, or whatever my timezone is now.
heart_rates = []
latitudes = []
longitudes = []
distances = []

# Get all data messages that are of type record
for record in fitfile.get_messages('record'):

    # Go through all the data entries in this record
    for record_data in record:
        
        if record_data.name == 'timestamp':
            timestamps.append(record_data.value)
        if record_data.name == 'position_lat':
            latitudes.append(record_data.value)
        if record_data.name == 'position_long':
            longitudes.append(record_data.value)
        if record_data.name == 'heart_rate':
            heart_rates.append(record_data.value)
        if record_data.name == 'distance':
            distances.append(record_data.value)
        
        """
        # Print the records name and value (and units if it has any)
        if record_data.units:
            print( " * %s: %s %s" % (
                record_data.name, record_data.value, record_data.units,
            ))
        else:
            print (" * %s: %s" % (record_data.name, record_data.value))
        """

df = pd.DataFrame(columns=['time','lat','lon','HR','distance'])

for i in range(0,len(timestamps)):
    
    lat = latitudes[i] * (10 ** (-7))
    lon = longitudes[i] * (10 ** (-7))
    
    row = [timestamps[i],lat,lon,heart_rates[i],distances[i]]
    a_row = pd.Series(row,index=df.columns)
    df = df.append(a_row,ignore_index=True)

time = timestamps[0]
file_name = 'activity_m{}.csv'.format(time)
    
df.to_csv(r'{}'.format(file_name))

import analyse

#print(analyse.best_time(1000,df))    

from datetime import timedelta
print(timestamps[0])
print(timestamps[1])
print(timestamps[2])
full = timestamps[-1] - timestamps[0]
print('Start time: ',timestamps[0])
print('Duration: ',full)
print('Distance: ',distances[-1])