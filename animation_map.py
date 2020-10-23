#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:48:49 2020

@author: WS
"""
"""
Using http://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/ and Paul for the appending, and myself for the removing first values.
"""

#import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import HTMLWriter

import pandas as pd

import analyse

import data_read as dr

import os

import shutil

shutil.rmtree('AABB0534_frames')

try:
    abbr_data = pd.read_csv(r'temp-abbr.csv')
    abbr_df = pd.DataFrame(abbr_data,columns=['abbr'])
    abbrs = abbr_df['abbr'].tolist()
    ac_abbr = abbrs[0]

except:
    users_data = pd.read_csv (r'users.csv')

    users_df = pd.DataFrame(users_data, columns= ['Initials'])
    
    initials = users_df['Initials'].tolist()[0]
    
    full = dr.pull_data(initials)
    acs = full['Activity number'].tolist()
    
    ac_abbr = acs[-1]
    
#ac_abbr = 'AABB0534'
    
route_df = analyse.route_data(ac_abbr)

#print('loading')

lons = route_df['lon'].tolist()
lats = route_df['lat'].tolist()

#print('thinning')

def process(vals):
    new = []
    for i in range(0,len(vals)):
        if (i % 15) == 0:
            new.append(vals[i])
        
        if i == len(vals) - 1 and (i % 15) != 0:
            new.append(vals[i])
            new.append(vals[i])
            new.append(vals[i])
        
    return(new)
    
lons = process(lons)
lats = process(lats)

x_route = []
y_route = []

#print(len(lons))

x_min = min(lons) - 0.0015
x_max = max(lons) + 0.0015
y_min = min(lats) - 0.0015
y_max = max(lats) + 0.0015

fig = plt.figure()
ax = plt.axes(xlim=(x_min, x_max), ylim=(y_min, y_max))
plt.axis('off')
line, = ax.plot([], [], lw=2,color='blue',ms=10)
#line_cos, = ax.plot([], [], lw=2,color='blue')

def init():    
    line.set_data([], [])
    #line_cos.set_data([], [])
    return line,
    #return line_cos,

def animate(i):
    #print('frame: ',i)
    x = lons[i]
    x_route.append(x)
    y = lats[i]
    y_route.append(y)
    #new_x = [x]
    #new_y = [y]
    #y_cos = np.cos(i * 0.02 & np.pi)
    line.set_data(x_route, y_route)
    #line_cos.set_data(x, y_cos)
    return line,
    #return line_cos,

#print(animate(10))

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(lons), interval=120, blit=True)

# set embed_frames=True to embed base64-encoded frames directly in the HTML
anim.save(f'{ac_abbr}.html', writer=HTMLWriter(embed_frames=False))

try:
    shutil.rmtree('AABB0534_frames')
except:
    print('No frames folder')
    

#plt.show()
"""
def process(vals):
    new = []
    for i in range(0,len(vals)):
        if (i % 15) == 0:
            new.append(vals[i])
        
        if i == len(vals) - 1 and (i % 15) != 0:
            new.append(vals[i])
            new.append(vals[i])
            new.append(vals[i])
        
    return(new)

def pullline():
    

def init():    
    
    line.set_data([], [])
    #line_cos.set_data([], [])
    return line,
    #return line_cos,

def sub_animate(i):
    print('frame: ',i)
    x = lons[i]
    x_route.append(x)
    y = lats[i]
    y_route.append(y)
    #new_x = [x]
    #print(x_route)
    #new_y = [y]
    #y_cos = np.cos(i * 0.02 & np.pi)
    line.set_data(x_route, y_route)
    #line_cos.set_data(x, y_cos)
    return line,

def animate_route(ac_df):

    lons = ac_df['lon'].tolist()
    lats = ac_df['lat'].tolist()

    print('thinning')

    lons = process(lons)
    lats = process(lats)

    x_route = []
    y_route = []

    print(len(lons))

    x_min = min(lons) - 0.0015
    x_max = max(lons) + 0.0015
    y_min = min(lats) - 0.0015
    y_max = max(lats) + 0.0015

    fig = plt.figure()
    ax = plt.axes(xlim=(x_min, x_max), ylim=(y_min, y_max))
    plt.axis('off')
    line, = ax.plot([], [], lw=2,color='blue',ms=10)
    #line_cos, = ax.plot([], [], lw=2,color='blue')

    init_line, = line.set_data([], [])
    
    #return line_cos,
    
    

    #print(animate(10))

    anim = animation.FuncAnimation(fig, sub_animate, init_func=init,
                               frames=len(lons), interval=120, blit=True)

# set embed_frames=True to embed base64-encoded frames directly in the HTML
    anim.save(f'{ac_abbr}.html', writer=HTMLWriter(embed_frames=False))
    
animate_route(route_df)
"""