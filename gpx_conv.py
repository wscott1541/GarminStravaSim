# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 13:05:01 2021

@author: wscot
"""
from datetime import datetime
from time import time

from numpy import NaN

import pandas as pd

from datetime import datetime
from time import time

def time_check():
    today = time()
    today_dt = datetime.fromtimestamp(today)
    time_string = datetime.strftime(today_dt,'%H:%M:%S')
    print(time_string)

time_check()

data = pd.read_csv('activity_B23I1958.csv')
#('activity_5187172776.csv')


df = pd.DataFrame(data,columns=['lon','lat','alt','time','distance','HR'])

#print(df.iloc[[905]])

time_check()

def create_nans(x):
    if str(x)[-8:] == '00:00:00':
        x = NaN
    return(x)


def best_time_ws(distance,gpx_df):
    print('start')
    time_check()
    distances = gpx_df['distance'].tolist()
    #times = gpx_df['time'].tolist()
    
    indexes = []
    
    for i in range(0,len(gpx_df)):
        
        if i % 1000 == 0:
            print(i)
        
        i_s = []
        
        for v in range(0,i):
            if len(i_s) < 1 and (distances[i] - distances[i-v]) > distance and (distances[i] - distances[i-v] < distance + 100):
                i_s.append(i-v)
                
        if len(i_s) > 0:
            indexes.append(i_s[0])
        else:
            indexes.append(i)#was NaN
    
    #gpx_df = gpx_df.index[gpx_df['distance'] < (distance - 1000)].tolist()[-1:]
    
    print('first loop')
    time_check()
    
    gpx_df[f'{distance} indexes'] = indexes
    
    #print(gpx_df)
    
    #print(type(gpx_df['time'][0]))
    gpx_df['time'] = gpx_df['time'].apply(lambda x : datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    #print(type(gpx_df['time'][0]))
    gpx_df[f'{distance} indexes'] = gpx_df[f'{distance} indexes'].apply(lambda x: int(x)) 
    
    #print(gpx_df[f'{distance} indexes'])
    #gpx_df = gpx_df.reset_index()
    #gpx_df['ref time'] = gpx_df['time'][gpx_df[f'{distance} indexes']]
    
    ref_times = []
    for i in range(0,len(gpx_df)):
        ref_time = gpx_df['time'][gpx_df[f'{distance} indexes'][i]]
        ref_times.append(ref_time)
    #print(len(ref_times))
    gpx_df['ref_times'] = ref_times
    
    gpx_df[f'{distance} time'] = gpx_df['time'] - gpx_df['ref_times']
    gpx_df[f'{distance} time'] = gpx_df[f'{distance} time'].apply(create_nans)
    print(gpx_df[f'{distance} time'].min())
    idx_end = gpx_df[f'{distance} time'].idxmin()
    idx_sta = gpx_df[f'{distance} indexes'][idx_end]
    #print(gpx_df[f'{distance} indexes'][idx_min])
    #print(gpx_df['time'][idx_min])
    #print(gpx_df['time'][1238])
    
    best = []
    for i in range(0,len(gpx_df)):
        if i < idx_sta:
            best.append(0)
        elif i > idx_end:
            best.append(2)
        else:
            best.append(1)
    
    gpx_df[f'{distance}'] = best
    
    gpx_df = gpx_df[['lon','lat','time','distance','alt','HR',f'{distance}']]#better with drop
    
    print(gpx_df)
    
    #gpx_df[f'{distance} time'] = gpx_df[f'{distance} time'].apply(create_nans)
#df.loc[df['Height'] <= 1.76]
    
#def getIndex (specific_dist,distance,specific_time,gpx_df):
#    bla = gpx_df.loc[gpx_df['time'] == specific_time]
#    newVal = gpx_df.index[gpx_df['distance'] < (specific_dist - distance)].max()
    
#    if (newVal):
#        return newVal[0]
#    return bla

def best_time_wm(distance,gpx_df):
    print('start')
    time_check()
    distances = gpx_df['distance'].tolist()
    times = gpx_df['time'].tolist()
    
    indexes = []
    
    gpx_df[f'{distance} index'] = gpx_df.apply(lambda x: getIndex(x['distance'],distance,x['time'],gpx_df), axis=0)
#df
    #gpx_df.loc[gpx_df['distance'] < (gpx_df['distance'] - distance)]['distance'][-1:]
    
    print(gpx_df[f'{distance} index'])
    
    print('first loop')
    time_check()
    
    #print(gpx_df)
    #gpx_df[f'{distance} indexes'] = indexes
    
    #print(gpx_df)
    
    #print(type(gpx_df['time'][0]))
    gpx_df['time'] = gpx_df['time'].apply(lambda x : datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    #print(type(gpx_df['time'][0]))
    
    #print(df[f'{distance} indexes'])
    
    #for i in range(0,)
    
    #gpx_df[f'{distance} indexes'] = df[f'{distance} indexes'].replace(NaN,str(df.index))
    
    print(gpx_df[f'{distance} indexes'])
    
    gpx_df[f'{distance} indexes'] = gpx_df[f'{distance} indexes'].apply(lambda x: int(x)) 
    
    #print(gpx_df[f'{distance} indexes'])
    #gpx_df = gpx_df.reset_index()
    #gpx_df['ref time'] = gpx_df['time'][gpx_df[f'{distance} indexes']]
    
    ref_times = []
    for i in range(0,len(gpx_df)):
        ref_time = gpx_df['time'][gpx_df[f'{distance} indexes'][i]]
        ref_times.append(ref_time)
    #print(len(ref_times))
    gpx_df['ref_times'] = ref_times
    
    gpx_df[f'{distance} time'] = gpx_df['time'] - gpx_df['ref_times']
    gpx_df[f'{distance} time'] = gpx_df[f'{distance} time'].apply(create_nans)
    print(gpx_df[f'{distance} time'].min())
    
    #gpx_df[f'{distance} time'] = gpx_df[f'{distance} time'].apply(create_nans)    

best_time_ws(1000,df)
print('finish')
time_check()

def getIndex (distance):
    noresult = "null"
    newVal = df.index[(df['distance'] < (distance - 1000))].max()  
    if (newVal):
        return newVal
    return noresult

def getIndex (x):
    noresult = df.index[df['distance'] == x['time']]#'null'

    newVal = df.index[(df['distance'] < (x['distance'] - 1000))].max()
    
    if str(newVal) != 'nan':
        return(newVal)
    #    return newVal
    else:
        
        return noresult
    
#df['1kmindex'] = df.apply(lambda x: getIndex(x), axis=1)

time_check()

#print(df.iloc[0]['1kmindex'])
#gpx_df.loc[gpx_df['time'] == specific_time]
#print(df.iloc[[35161]])
#print(df.iloc[[34613]]['time'])