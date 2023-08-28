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
import json

import pandas as pd
from datetime import datetime
from dateutil import relativedelta
from typing import Optional

from .GSSutils import data_read as dr
from .GSSutils import primary_functions as pf
from .GSSutils import today_string as ts
from .GSSutils import analyse as af

from .GSSutils import editing as ef
from .GSSutils import notes as notes

from .GSSutils import basic_functions as bf

from .GSSutils import mapper

from .GSSutils import challenges

def get_time():
    from time import time
    now = time()
    return(datetime.strftime(datetime.fromtimestamp(now)+relativedelta.relativedelta(hours=1),'%Y-%m-%d %H:%M:%S'))

def action_log(action_dictionary)->None:
    fileDir = os.path.dirname(os.path.realpath('__file__'))

    filename = os.path.join(fileDir, 'usage_log.csv')
    
    try:
        data = pd.read_csv(filename)
        log = pd.DataFrame(data,columns=['timestamp','page_type','detail','mode'])
    except:
        log = pd.DataFrame(columns=['timestamp','page_type','detail','mode'])
        
    if len(log) >= 1:
        mode = log['mode'].tolist()[-1]
    else:
        mode = 'user'#will want to finalise what I want to do here
        
    action_dictionary['timestamp'] = [get_time()]
    action_dictionary['mode'] = [mode]
        
    action_df = pd.DataFrame.from_dict(action_dictionary)
    log = log.append(action_df)
    log.to_csv(r'{}'.format(filename))


def chart_as_html():
    plt.savefig('temp_image.jpg')
    
    encoded = base64.b64encode(open('temp_image.jpg','rb').read()).decode()
    
    img = f"""\
<img src='data:image/jpg;base64,{encoded}'>
"""
    
    os.remove('temp_image.jpg')
    
    
    return(img)

def index_list():
    df = dr.pull_data()
    
    abbrs = df['Activity number'].tolist()
    types = df['Activity Type'].tolist()
    dates = df['Date'].tolist()
    times = df['Time'].tolist()
    dists = df['Distance'].tolist()
    rankings = df['Run Rankings'].tolist()
    notes = df['Notes'].apply(lambda x: x if x==x else '').tolist()
    shoes = df['Shoes'].apply(pf.shoes_specific_line).tolist()
    
    table = '''<table style='width: 100%'>
<th>Activity ID</th>
<th>Type</th>
<th>Date</th>
<th>Duration</th>
<th>Distance, km</th>
<th class='notes-col'>Notes</th>
<th>Shoes</th>
<th></th>'''
    
    
    for i in range(0,len(df)):
        v = len(df) - i - 1
        
        row = f"""<tr>
<td><a href='{abbrs[v]}'>{abbrs[v]}</a></td>
<td>{types[v]}</td>
<td>{dates[v]}</td>
<td>{times[v]}</td>
<td>{dists[v]}</td>
<td class='notes-col'>{notes[v]}</td>
<td>{shoes[v]}</td>
<td>{pf.interpret_rankings(rankings[v])}</td>
</tr>"""

        table = table + row
    
    return(table)

        
def generate_map(activity,map_size='reg'):
    
    activity_type = dr.ac_detail(activity, 'Activity Type')

    if activity_type != 'Cardio':
        activity_df = dr.route_data(activity)
    
        #mapper.tmb_test(activity_df,plot_size = map_size)
    
        #chart = chart_as_html()
    
        chart = mapper.enhanced_plotly_osm_map(activity_df)
    else:
        chart = ''
    
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
    if dr.ac_detail(ac_no, 'Activity Type') == 'Running' and dr.ac_detail(ac_no, 'Distance') >=2.4:
        user_df = dr.pull_data()
        try:
            pf.times_radar(user_df, ac_no)
            chart = chart_as_html()
        except:
            chart = ''
        #lines = pf.cropped_activity_lines(user_df, ac_no)
        #chart = f'<p>{lines}<br>{chart}</p>'
        #lines = pf.cropped_activity_table(user_df, ac_no)
        #chart = f'{lines}<p>{chart}</p>'
        #chart = f'<p>{lines}<br>{chart}</p>'
    else:
        chart = ''
        
    return(chart)
    
def otd_para(date=ts.today_string):
    
    user_df = dr.pull_data()
    
    para = pf.otd_html_folium(date,user_df,img = 'Y')
    
    return(para)

def month_and_previous_running_distances(day=ts.day, month=ts.month, year=ts.year):
    
    user_df = dr.pull_data()
    
    pf.plot_month_previous_distances(day, month, year, 'Running', user_df)
    
    chart = chart_as_html()
    
    return(chart)

def week_and_previous_running_distances(date_string=ts.today_string):

    user_df = dr.pull_data()
    
    pf.plot_week_previous_distances(user_df,date_string,'Running')
    
    chart = chart_as_html()
    
    return(chart)

def latest_activity():
    df = dr.pull_data()
    
    abbr = df['Activity number'].tolist()[-1]
    
    ac = dr.Activity(abbr)
    
    ac_type = df['Activity Type'].tolist()[-1]
    date = ac.date_str
    time = df['Time'].tolist()[-1]
    dist = df['Distance'].tolist()[-1]
    rankings = df['Run Rankings'].tolist()[-1]
    
    try:
        ac_map = mapper.plot_osm_map(ac.route_data, 40, 40)
        map_html = f'<br>{ac_map}'
    except:
        map_html = ''
    
    link = f"<a href='/index/{abbr}'>{ac_type}</a>"
    
    html = f'''<b><u>Latest</u></b><br>
{link}, {date}<br>
{dist}km, {time} {pf.interpret_rankings(rankings)}
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

def year_distances(year:int=ts.year, month:Optional[int]=None, activity:Optional[str]='Running'):
    
    if month is None:
        if year == ts.year:
            month = ts.month
        else:
            month = 12#effectively default to December if the year has been completed
    
    df = dr.pull_data()
    
    chart = pf.plotly_distances_this_year_and_last(df, month, year, activity)
    
    return chart

def activity_page_title(ac_no):
    ac_type = dr.ac_detail(ac_no, 'Activity Type')
    ac_date = dr.ac_detail(ac_no, 'Date')
    
    title = f'{ac_type}, {ac_date}'
    
    return(title)

def activity_otd(ac_no):
    
    user_df = dr.pull_data()
    
    ac_date = str(dr.ac_detail(ac_no, 'Date'))[:10]
    try:
        para = pf.otd_html_folium(ac_date,user_df,img = 'Y',index_link = False)
    except:
        para = ''
    
    return(para)
    
def split_rankings(distance):
            
    dist = bf.durl_to_dtag(distance)
        
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

def split_page_title(ac_no, distance, html=False):

    user_df = dr.pull_data()
        
    split = pf.formatted_title(distance)

    date = dr.activity_details(user_df,ac_no,'Date')
    date = datetime.strftime(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d') 
    
    time = str(dr.activity_details(user_df,ac_no,split)).replace('0 days ','')

    if html:
        return f'''<b>{split}</b>: {time} on {date}'''
    else:
        return split + ': ' + date
    
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
    shoes = dr.ac_detail(ac_no, 'Shoes')

    if shoes == shoes:      
        line = pf.shoes_activity_line(user_df,ac_no)
    else:
        line = ''
    
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

def edit_prompt(field):
    
    user_df = dr.pull_data()
    
    prompt = ef.edit_prompt(user_df, field)
    
    return prompt

def return_edit(ac_no, field, new_string, activity):
    
    user_df = dr.pull_data()
    
    line = ef.edit_field(user_df, ac_no, field, new_string, activity)
    
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

def challenge_title(challenge):
    
    if challenge in challenges.challenge_list:
        s = challenges.translate_title(challenge)
    else:
        s = challenge
        
    return s

def challenge_map(challenge):
    
    user_df = dr.pull_data()
    yyyy = ts.year
    
    if challenge in challenges.challenge_list:
        div = challenges.challenge(yyyy, user_df,challenge)
    else:
        div = ''
    
    return(div)

def challenge_progress(challenge):
    
    user_df = dr.pull_data()
    yyyy = ts.year
    
    if challenge in challenges.challenge_list:
        div = challenges.plot_challenge_linear_progress(challenge,user_df,yyyy)
    else:
        div = ''
        
    return(div)

def challenge_summary(challenge):
    
    user_df = dr.pull_data()
    yyyy = ts.year
    
    if challenge in challenges.challenge_list:
        s = challenges.challenge_summary(challenge,user_df,yyyy)
    else:
        s = f'There is no challenge associated with {challenge}.'
        
    return s
    
def challenge_table(challenge):
    
    user_df = dr.pull_data()
    
    if challenge in challenges.challenge_list:
        table = challenges.waymark_table(challenge, user_df)
    else:
        table = ''
        
    return table
    

def hr_pie(ac_no):
    
    ac_df = dr.route_data(ac_no)
    
    try:    
        div = af.hr_zones_pie_plotly(ac_df)
    except:
        div='<p>No HR data</p>'
    
    return(div)

def hr_dist(ac_no):
    
    ac_df = dr.route_data(ac_no)
    
    try:
        af.hr_distribution(ac_df)
    
        chart = chart_as_html()
    except:
        chart = '<p>No HR data</p>'
    
    return(chart)


def ThreeD_map(ac_no):
    
    ac_df = dr.route_data(ac_no)
    activity_type = dr.ac_detail(ac_no,'Activity Type')

    if activity_type != 'Cardio':   
        div = mapper.basic_3D_map_plotly(ac_df)
    else:
        div = ''
    
    return(div)

def challenge_update(ac_no):
    
    user_df = dr.pull_data()
    
    update = '<b><u>Challenges</u></b><br>'
    
    for c in challenges.challenge_list:
        c_update = challenges.challenge_update(ac_no,user_df,c)
        update += c_update
        
        if c != challenges.challenge_list[-1]:
            update += '<br>'
    
    html = f'<p>{update}</p>'
    
    return(html)

def activity_notes(ac_no):
    
    div = notes.load_notes_html(ac_no)
    
    return div

def km_split_bars(ac_no, distance=None, whole_activity=True):
    
    ac_df = dr.route_data(ac_no)
    activity_type = dr.ac_detail(ac_no,'Activity Type')
    
    if activity_type in ('Running'):
        div = af.km_splits_bars_plotly(ac_df, distance, whole_activity)
    else:
        div = ''
    
    return div

def halfway_split_p(ac_no, distance):
    
    ac_df = dr.route_data(ac_no)
    activity_type = dr.ac_detail(ac_no,'Activity Type')
    
    if activity_type in ('Running'):
        front, back, diff = af.halfway_split_str(ac_df, distance)
        
        p = f'''Front half: {front}
<br>Back half: {back}
<br>Difference: {diff}
'''
    else:
        p = ''
    
    return p

def split_reigel_efficiency(ac_no, distance):
    
    user_df = dr.pull_data()
    
    return af.distance_reigel_efficiency(user_df, ac_no, distance)

def run_rankings_html_str(ac_no):
    
    return pf.interpret_rankings(dr.ac_detail(ac_no, 'Run Rankings'))

def rise_and_fall(ac: dr.Activity)->str:
    
    if ac.ascent_str and ac.descent_str:
        return f'<br>{ac.ascent_str} up, {ac.descent_str} down'
    else:
        return ''

def pb_summary_paras(activities: dr.Activities, join:Optional[str]='<br>')->str:
    
    pbs = {}
    
    for d in dr.dist_list:
        ac_id = activities.pb_activity(d)
        
        if ac_id:
        
            ac_obj = dr.Activity(ac_id)
            n_pbs = activities.n_pbs(d)
            n_pbs_str = '' if n_pbs == 0 else f'({n_pbs} PBs)'
            pbs[d] = {
                'time': activities.quickest_time(d),
                'date': f"{ac_obj.day} {ac_obj.strftime('%b')}",
                'link': f'../../index/{ac_id}',
                'n_pbs': n_pbs_str}
        
    strs = []
    
    for k,d in pbs.items():
        if d['time']:
            strs.append(f"{k}: {d['time'].replace('0 days ', '')} on <a href='{d['link']}'>{d['date']}</a> {d['n_pbs']}")
    
    return join.join(strs)