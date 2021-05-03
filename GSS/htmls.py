# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 10:48:10 2021

@author: WS
"""

#import pandas as pd

#import mpld3

import base64
import os

import matplotlib.pyplot as plt

from .GSSutils import data_read as dr
from .GSSutils import primary_functions as pf
from .GSSutils import today_string as ts
from .GSSutils import analyse as af
#print(ts.today_string)
#from . import analyse
from .GSSutils import editing as ef

from .GSSutils import basic_functions as bf

from .GSSutils import mapper

from .GSSutils import challenges

#def chart_from_mpl():
    
#    fig = plt.gcf()
    
#    chart = mpld3.fig_to_html(fig)
    
    #plt.show()
    
#    return(chart)

def chart_as_html():
    plt.savefig('temp_image.jpg')
    
    encoded = base64.b64encode(open('temp_image.jpg','rb').read()).decode()
    
    img = f"""\
<img src='data:image/jpg;base64,{encoded}'>
"""
    
    os.remove('temp_image.jpg')
    
    #plt.show()
    
    #img = chart_from_mpl()
    
    return(img)

def index_list():
    df = dr.pull_data()
    #df = dr.pull_data()
    
    abbrs = df['Activity number'].tolist()
    types = df['Activity Type'].tolist()
    dates = df['Date'].tolist()
    times = df['Time'].tolist()
    dists = df['Distance'].tolist()
    
    table = '''<table>
<th>Activity ID</th>
<th>Type</th>
<th>Date</th>
<th>Duration</th>
<th>Distance, km</th>'''
    
    #body = body + "<a href='{abbrs[-1]}'>{abbrs[-1]}</a>: {types[-1]}, {dates[-1]}: {dists[-1]}, {times[-1]}"
    
    for i in range(0,len(df)):
        v = len(df) - i - 1
        
        row = f"""<tr>
<td><a href='{abbrs[v]}'>{abbrs[v]}</a></td>
<td>{types[v]}</td>
<td>{dates[v]}</td>
<td>{times[v]}</td>
<td>{dists[v]}</td>
</tr>"""
        #if i != len(df) - 1:
        #    line = line + '<br>'
        #body = body + line
        table = table + row
    
    return(table)

####print(index_list)
        
def generate_map(activity,map_size='reg'):
    
    activity_df = dr.route_data(activity)
    
    #mapper.tmb_test(activity_df,plot_size = map_size)
    
    #chart = chart_as_html()
    
    chart = mapper.enhanced_plotly_osm_map(activity_df)
    
    #chart = mapper.plot_osm_map(activity_df)
        
    return(chart)

def times_table(ac_no):
    if dr.ac_detail(ac_no, 'Activity Type') == 'Running':
        user_df = dr.pull_data()
        #pf.times_radar(user_df, ac_no)
        #chart = chart_as_html()
        #lines = pf.cropped_activity_lines(user_df, ac_no)
        #chart = f'<p>{lines}<br>{chart}</p>'
        table = '<br>' + pf.cropped_activity_table(user_df, ac_no)
        
        #chart = f'<p>{lines}<br>{chart}</p>'
    else:
        table = ''
        
    return(table)

def times_radar(ac_no):
    if dr.ac_detail(ac_no, 'Activity Type') == 'Running':
        user_df = dr.pull_data()
        pf.times_radar(user_df, ac_no)
        chart = chart_as_html()
        #lines = pf.cropped_activity_lines(user_df, ac_no)
        #chart = f'<p>{lines}<br>{chart}</p>'
        #lines = pf.cropped_activity_table(user_df, ac_no)
        #chart = f'{lines}<p>{chart}</p>'
        #chart = f'<p>{lines}<br>{chart}</p>'
    else:
        chart = ''
        
    return(chart)
    
def otd_para(date=ts.today_string):
    #print(str(ts.today_string))
    user_df = dr.pull_data()
    
    para = pf.otd_html_folium(date,user_df,img = 'Y')
    
    return(para)

def month_and_previous_running_distances():
    print('month and prevous')
    bf.time_check()
    
    user_df = dr.pull_data()
    
    pf.plot_month_previous_distances(ts.month,ts.year,'Running',user_df)
    
    chart = chart_as_html()
    
    bf.time_check()
    
    return(chart)

def week_and_previous_running_distances():
    print('week and previous')
    bf.time_check()
    user_df = dr.pull_data()
    
    pf.plot_week_previous_distances(user_df,ts.today_string,'Running')
    
    chart = chart_as_html()
    
    bf.time_check()
    
    return(chart)

def latest_activity():
    df = dr.pull_data()
    
    abbr = df['Activity number'].tolist()[-1]
    ac_type = df['Activity Type'].tolist()[-1]
    date = df['Date'].tolist()[-1]
    time = df['Time'].tolist()[-1]
    dist = df['Distance'].tolist()[-1]
    
    try:
        ac_df = dr.route_data(abbr)
        ac_map = mapper.plot_osm_map(ac_df,40,40)
        map_html = f'<br>{ac_map}'
    except:
        map_html = ''
    
    link = f"<a href='/index/{abbr}'>{ac_type}</a>"
    
    html = f'''<b><u>Latest</u></b><br>
{link}, {date}<br>
{dist}km, {time}
{map_html}'''

    return(html)

def year_week_progress():
    #print('year week')
    #bf.time_check()
    df = dr.pull_data()
    
    pf.plot_rolling_year_week_progress(df,'Running',ts.today_string)

    chart = chart_as_html()    
    #bf.time_check()
    return(chart)

def year_distances():
    #print('year dists')
    #bf.time_check()
    df = dr.pull_data()
    
    pf.plot_distances_this_year(df,ts.month,ts.year,'Running')
    
    chart = chart_as_html()
    #bf.time_check()
    return(chart)

def activity_page_title(ac_no):
    ac_type = dr.ac_detail(ac_no, 'Activity Type')
    ac_date = dr.ac_detail(ac_no, 'Date')
    
    title = f'{ac_type}, {ac_date}'
    
    return(title)

def activity_otd(ac_no):
    
    user_df = dr.pull_data()
    
    ac_date = str(dr.ac_detail(ac_no, 'Date'))[:10]
    
    para = pf.otd_html_folium(ac_date,user_df,img = 'Y',index_link = False)
    
    return(para)
    
def split_rankings(distance):
    
    if distance == '1mile':
        dist = '1 mile'
    elif distance == '1.5mile':
        dist = '1.5 mile'
    elif distance == '3mile':
        dist = '3 mile'
    else:
        dist = distance
        
    user_df = dr.pull_data()
    
    table = pf.rankings_html(user_df,dist)
    
    return(table)

def top_para():
    
    user_df = dr.pull_data()
    
    para = pf.top_n(user_df,n=5)
    
    return(para)

def split_title(distance):
    
    title = pf.formatted_title(distance)
    
    return(title)

'''
def split_plot(distance):
    
    user_df = dr.pull_data()
    
    pf.splits_plot(user_df,distance)
    
    chart = chart_from_mpl()
    
    pos = chart.find('<div')
    
    chart = chart[pos:]
    
    
    #title = f'<u><b>{d}</b></u>'
    
    #full = title + chart
    
    return(chart)
'''

def distance_pace_plot(ac_no):
    df = dr.route_data(ac_no)
    
    af.distance_pace(df)
    
    chart = chart_as_html()
    
    return(chart)
    
def distance_map(ac_no,distance):

    d = bf.durl_to_dtag(distance)    

    ac_df = dr.route_data(ac_no,d)   
    
    chart = mapper.stretch_osm_map(ac_df, d, width_input=80, height_input=80)
    
    return(chart)

def comparisons(ac_no):
    
    user_df = dr.pull_data()
    
    div = pf.activity_comparisons_plotly(user_df, ac_no)
    
    return(div)

def times_curve(ac_no):
    
    if dr.ac_detail(ac_no, 'Activity Type') == 'Running':
        user_df = dr.pull_data()
        pf.times_curve(user_df, ac_no)
        chart = chart_as_html()
    else:
        chart = ''
        
    return(chart)

def all_splits_plot():
    
    user_df = dr.pull_data()
    
    div = pf.all_splits_plot(user_df)
    
    return(div)

def splits_plotly(distance):
    
    user_df = dr.pull_data()
    
    dtag = bf.durl_to_dtag(distance)
    
    div = pf.all_splits_plot(user_df,dtag) + '<br>'

    
    return(div)

def prev_post(ac_no):
    
    user_df = dr.pull_data()
    
    line = pf.prev_next(ac_no,user_df)
    
    return(line)

def map_bt_line(ac_no):
    
    user_df = dr.pull_data()
    
    line = pf.distances_options(user_df,ac_no)
    
    return(line)

def shoes_activity(ac_no):
    user_df = dr.pull_data()
    
    line = pf.shoes_activity_line(user_df,ac_no)
    
    return(line)

def shoes_table():
    
    user_df = dr.pull_data()
    
    rows = pf.shoe_rows(user_df)
    
    return(rows)

def shoes_plot():
    
    user_df = dr.pull_data()
    
    div = pf.shoes_plotly(user_df)
    
    return(div)

def pace_alt_plotly(ac_no):
    
    ac_df = dr.route_data(ac_no)
    
    #div = af.pace_alt_distance_plotly(ac_df)
    
    div = af.distance_plotly(ac_df)
    
    return(div)

def return_edit(ac_no,field,new_string):
    
    user_df = dr.pull_data()
    
    line = ef.edit_field(user_df,ac_no,field,new_string)
    
    return(line)

def get_note(ac_no):
    
    note = dr.ac_detail(ac_no, 'Notes')
    
    note = str(note)
    
    if note == 'nan':
        out = ''
    elif len(note) > 1:
        out = note + '<br>'
        
    else:
        out = ''
        
    return(out)

def challenge_map(challenge):
    
    user_df = dr.pull_data()
    yyyy = ts.year
    
    if challenge == 'lejog':
        div = challenges.lejog(yyyy, user_df)
    else:
        div = ''
    
    return(div)

def hr_pie(ac_no):
    
    ac_df = dr.route_data(ac_no)
        
    div = af.hr_zones_pie_plotly(ac_df)
    
    return(div)

def hr_dist(ac_no):
    
    ac_df = dr.route_data(ac_no)
    
    af.hr_distribution(ac_df)
    
    chart = chart_as_html()
    
    return(chart)


def ThreeD_map(ac_no):
    
    ac_df = dr.route_data(ac_no)
    
    div = mapper.basic_3D_map_plotly(ac_df)
    
    return(div)

def challenge_update(ac_no):
    
    user_df = dr.pull_data()
    
    update = challenges.lejog_update(ac_no,user_df)
    
    html = f'<p>{update}</p>'
    
    return(html)