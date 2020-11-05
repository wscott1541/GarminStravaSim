#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 13:04:03 2020

@author: WS
"""

import smtplib, ssl

from primary_user_functions import month_caller
import matplotlib.pyplot as plt

import urllib

import base64
import os

import pandas as pd

sd_csv = pd.read_csv (r'email_settings.csv')

sd_df = pd.DataFrame(sd_csv, columns= ['smtp server','Port','Email','Password'])

ss_list = sd_df['smtp server'].tolist()  
smtp_server = ss_list[0]

port_list = sd_df['Port'].tolist()
port = round(float(port_list[0]))

se_list = sd_df['Email'].tolist()
sender_email = se_list[0]

pw_list = sd_df['Password'].tolist()
password = pw_list[0]

users_data = pd.read_csv (r'users.csv')

users_df = pd.DataFrame(users_data, columns= ['Username','Initials'])
users_list = users_df['Username'].tolist()
receiver_email = users_list[0]

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from today_string import day, month, year, today_string, y_day_string

import data_read as dr

initials = users_df['Initials'].tolist()[0]

dates,distances,durations,types = dr.data_read(initials)

date = dates[-1]

try:
    abbr_data = pd.read_csv(r'temp-abbr.csv')
    abbr_df = pd.DataFrame(abbr_data,columns=['abbr'])
    abbrs = abbr_df['abbr'].tolist()
    ac_abbr = abbrs[0]
    add_animation = True
except:
    full = dr.pull_data(initials)
    acs = full['Activity number'].tolist()
    
    ac_abbr = acs[-1]
    
    add_animation = False

user_df = dr.pull_data(initials)

ac_type = dr.activity_details(user_df,ac_abbr,'Type')

import analyse

noun,verb,plural = analyse.words(ac_type)

subject = "{} {}".format(noun.capitalize(),date)

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

import mapper

import primary_user_functions as puf

if ac_type != 'Cardio':
    ac_route = analyse.route_data(ac_abbr)

#body = puf.html_assessment(user_df,ac_abbr)

def chart_as_html():
    plt.savefig('temp_image.jpg')
    
    encoded = base64.b64encode(open('temp_image.jpg','rb').read()).decode()
    
    img = f"""\
<body>
   <img src='data:image/jpg;base64,{encoded}'>
</body>
"""
    
    #new = body + img

    #part = MIMEText(html, "html")
    #message.attach(part)
    
    #new = body + img
    
    os.remove('temp_image.jpg')
    
    plt.show()
    
    return(img)

def attach_chart_as_html(body):
    plt.savefig('temp_image.jpg')
    
    encoded = base64.b64encode(open('temp_image.jpg','rb').read()).decode()
    
    img = f"""\
<body>
   <img src='data:image/jpg;base64,{encoded}'>
</body>
"""
    
    #new = body + img

    #part = MIMEText(html, "html")
    #message.attach(part)
    
    new = body + img
    
    os.remove('temp_image.jpg')
    
    plt.show()
    
    return(new)

plt.show()

def attach_animation():
    
    #anim = codecs.open("animation.html", "r", "utf-8")
    
    #anim = base64.b64encode(open('animation.html','rb').read()).decode()
    #urllib.urlopen("animation.html").read()# encoded = base64.b64encode(open('animation.html','rb').read()).decode()
    
    temp_anim = pd.DataFrame(columns= ['abbr'])

    row = [ac_abbr]
    a_row = pd.Series(row,index=temp_anim.columns)
    temp_anim = temp_anim.append(a_row,ignore_index=True)
    
    temp_anim.to_csv(r'temp-animation.csv',index=False)
    
    print('Loading animation')
    
    import animation_map
    
    anim = MIMEApplication(open(f"{ac_abbr}.html", "rb").read())
    anim.add_header('Content-Disposition', 'attachment', filename=f"{ac_abbr}.html")
    message.attach(anim)
    
    os.remove(f'{ac_abbr}.html')
    
    os.remove(f'temp-animation.csv')
    #message.attach(MIMEText(anim,'html'))
    
    #return(anim)
    
if ac_type != 'Cardio':
    
    
    mapper.pyplot_colourmap(ac_route)
    body = chart_as_html()
    
    #body = add_animation()
    
    body = body + puf.html_assessment(user_df,ac_abbr)
    
    puf.activity_comparisons(user_df,ac_abbr)
    body = attach_chart_as_html(body)
    
    #ac_route = analyse.route_data(ac_abbr)
    mapper.pyplot_heatmap(ac_route)
    body = attach_chart_as_html(body)
    
    if ac_type == 'Running':
        mapper.best_stretch_map(ac_route,1000)
    else:
        try:        
            mapper.best_stretch_map(ac_route,5000)
        except:
            mapper.best_stretch_map(ac_route,1000)
    body = attach_chart_as_html(body)
    
    try:
        analyse.hr_dist_speed_plot(ac_route)
        body = attach_chart_as_html(body)
    except:
        print('No HR')
    analyse.lap_bars(ac_route)
    body = attach_chart_as_html(body)
    
    mapper.pyplot_basic(ac_route)
    body = attach_chart_as_html(body)
    #analyse.hr_plot_time(ac_route)
    #body = attach_chart_as_html(body)
    #analyse.hr_plot_dist(ac_route)      
    #body = attach_chart_as_html(body)
    try:
        analyse.hr_dist_durs_plot(ac_route)
        body = attach_chart_as_html(body)
        analyse.hr_zones_pie(ac_route)
        body = attach_chart_as_html(body)
        analyse.hr_distribution(ac_route)
        body = attach_chart_as_html(body)
        body = body + analyse.hr_html(ac_route)
    except:
        print('No HR')
    puf.plot_week_and_previous_distances(today_string,ac_type)
    body = attach_chart_as_html(body)
    ac_df = dr.pull_data(initials)
    puf.plot_week_previous_durations(ac_df,date,ac_type)
    body = attach_chart_as_html(body)
    puf.plot_month_and_previous_distances(month,year,ac_type)#would be nice to redo by date
    body = attach_chart_as_html(body)
    
    if add_animation == True and ac_type == 'Running':
        attach_animation()
    
else:
    body = puf.html_assessment(user_df,ac_abbr)
    ac_route = analyse.route_data(ac_abbr)
    analyse.hr_plot_time(ac_route)
    body = attach_chart_as_html(body)
    analyse.hr_zones_pie(ac_route)
    body = attach_chart_as_html(body)
    analyse.hr_distribution(ac_route)
    body = attach_chart_as_html(body)
    body = body + analyse.hr_html(ac_route)
    ac_df = dr.pull_data(initials)
    puf.plot_week_previous_durations(ac_df,date,ac_type)
    body = attach_chart_as_html(body)

reference = f"""<body><p>
Ref: <i>{ac_abbr}</i></p></body>"""
    
if ac_type == 'Running' or ac_type == 'Cycling':
    outtro = puf.all_personal_bests_html()
    #message.attach(MIMEText(outtro, "html"))

    final = body + outtro + reference
else:
    final = body + reference

html = f"""<html>
{final}
</html>
"""

message.attach(MIMEText(html,'html'))

"""Complete and send email"""

text = message.as_string()

context = ssl.create_default_context()
print('Sending...')
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
        
print('Sent to {}'.format(receiver_email))

try:
    os.remove('temp-abbr.csv')
except:
    print('No temp csv')

try:
    os.remove(f'{ac_abbr}.FIT')
except:
    print('No FIT file')
