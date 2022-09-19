#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 14:43:01 2022

@author: willscott
"""

import pandas as pd

from typing import Dict, List

data = pd.read_csv('activities.csv')

df = pd.DataFrame(data)

dist_dict = {'1km': 1000,
              '1 mile': 1609.34,
              '1.5 mile': 2414.02,
              '3 mile': 4828.03,
              '5km': 5000,
              '5 mile': 8046.72,
              '10km': 10000,
              '10 mile': 16093.40,
              '20km': 20000,
              'Half': 21097.7,
              'Full': 42195}

def add_rankings(x: pd.DataFrame) -> Dict[str, List[str]]:
    rankings = None
    rankings = {
        '1st': [],
        '2nd': [],
        '3rd': []
        }
    
    for dist in dist_dict:
        time = x[dist]
        date = x['Date']
        a_type = x['Activity Type']
        
        d_df = df[(df['Date']<date)&(df[dist]<=time)&(df[dist]!='NONE')]
        
        #if '2022-09-17' in str(date) and dist == '1.5 mile':
        #    print(d_df, d_df[dist].unique())
        
        if a_type != 'Running':
            rankings = {}
        elif time == 'NONE':
            pass
        elif len(d_df[dist].unique()) == 0:
            rankings['1st'].append(dist)
        elif len(d_df[dist].unique()) == 1:
            rankings['2nd'].append(dist)
        elif len(d_df[dist].unique()) == 2:
            rankings['3rd'].append(dist)
    
    return rankings

#df = df.head()

df['Run Rankings'] = df.apply(add_rankings, axis=1)

cols = ['Activity number','Activity Type','Date','Distance','Time','Shoes','Rise','Fall','1km','1 mile','1.5 mile','3 mile','5km','5 mile','10km','10 mile','20km','Half','Full','C10k','C20k','C50k','C100k','C200k','C250k','Run Rankings','Notes','Admin']

df = df[cols]

print(df.head(), print(df.tail()))

df.to_csv('activities.csv')

    