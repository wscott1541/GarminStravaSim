#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 13:04:03 2020

@author: WS
"""

import smtplib, ssl

import primary_user_functions as puf
from primary_user_functions import month_caller
import multiple_user_functions as muf
import matplotlib.pyplot as plt

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

users_df = pd.DataFrame(users_data, columns= ['Username'])
users_list = users_df['Username'].tolist()
receiver_email = users_list[0]

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from today_string import day, month, year, today_string, y_day_string

subject = "SNEUE, {} {} {}".format(day,month_caller(month),year)

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

#intro = "Maybe one day this will also provide text insights. "
#message.attach(MIMEText(intro, "plain"))

intro = puf.week_summary_html()
message.attach(MIMEText(intro,'html'))

def attach_chart_as_html():
    plt.savefig('temp_image.jpg')
    
    encoded = base64.b64encode(open('temp_image.jpg','rb').read()).decode()
    
    html = f"""\
<html>
 <body>
   <img src='data:image/jpg;base64,{encoded}'>
 </body>
</html>
"""
    
    part = MIMEText(html, "html")
    message.attach(part)
    
    os.remove('temp_image.jpg')
    

"""List functions to send"""
puf.plot_month_distance(month,year,'Running')
attach_chart_as_html()
puf.plot_month_and_previous_distances(month,year,'Running')
attach_chart_as_html()
puf.plot_month_and_previous_durations(month,year,'Running')
attach_chart_as_html()
puf.plot_month_and_previous_distances(month,year,'Cycling')
attach_chart_as_html()
puf.plot_month_and_previous_distances(month,year,'Walking')
attach_chart_as_html()
puf.plot_distances_this_year(month,year,'Running')
attach_chart_as_html()
puf.plot_durations_all_previous(month,year,'Running')
attach_chart_as_html()
puf.plot_distances_all_previous(month,year,'Running')
attach_chart_as_html()
puf.plot_cumulative_distance(month,year,'Running')
attach_chart_as_html()
puf.plot_cumulative_distance(month,year,'All')
attach_chart_as_html()
puf.plot_week_and_previous_distances(y_day_string,'Running')
attach_chart_as_html()  
puf.plot_week_and_previous_distances(y_day_string,'Cycling')
attach_chart_as_html() 
puf.plot_week_and_previous_distances(y_day_string,'All')
attach_chart_as_html()      

muf.plot_month_distances(month,year,'Running')
attach_chart_as_html()
muf.plot_distances_this_week(y_day_string,'Running')
attach_chart_as_html()

outtro = puf.all_personal_bests_html()
message.attach(MIMEText(outtro, "html"))

"""Complete and send email"""

text = message.as_string()

context = ssl.create_default_context()
print('Sending...')
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
        
print('Sent to {}'.format(receiver_email))


   


