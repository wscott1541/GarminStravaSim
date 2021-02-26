# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 09:03:26 2021

@author: WS
"""

#import pandas as pd

#from . import data_read as dr
    
def nan_to_none(x):
    
    if str(x) == 'nan' or str(x) == 'NONE':
        x = ''
        
    return(x)

def format_url(x):
    
    if 'str' in str(type(x)):
        x = x.replace('_',' ')
        x = x[:1].upper() + x[1:]
        
    return(x)

def edit_field(user_df,activity_number,column,new):
    
    location = user_df.loc[user_df['Activity number'] == activity_number].index.values[0]

    allowed = ['Notes','Admin','Activity Type','Shoes']#At some point do type, but, for the moment, that contains a space

    column = format_url(column)

    if column in allowed:
        
        print(user_df[column].dtype)
        
        if '64' in str(user_df[column].dtype):
            user_df[column] = user_df[column].apply(lambda x: str(x))
        
        user_df[column] = user_df[column].apply(nan_to_none)
        
        new = format_url(new)
        
        user_df.at[location,column] = new
        
        user_df.to_csv('activities.csv', index = False)
        
        out = 'Edit complete'

    else:
        out = f'{column} not editable'
        
    return(out)

    
    