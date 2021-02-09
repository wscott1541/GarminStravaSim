# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:37:14 2021

@author: wscot
"""

import smtplib, ssl

from primary_user_functions import month_caller
import matplotlib.pyplot as plt

import urllib

import base64
import os

import pandas as pd

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from today_string import day, month, year, today_string, y_day_string

import data_read as dr

import analyse

import mapper

import primary_user_functions as puf

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
    plt.savefig('temp_image.jpg')#bbox_inches = 'tight'
    
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

'''
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
'''    

def load_settings():
    sd_csv = pd.read_csv (r'email_settings.csv')
    sd_df = pd.DataFrame(sd_csv, columns= ['smtp server','Port','Email','Password'])
    ss_list = sd_df['smtp server'].tolist()  
    smtp_server = ss_list[0]
    port_list = sd_df['Port'].tolist()
    port = round(float(port_list[0]))
    
    se_list = sd_df['Email'].tolist()
    sender_email = se_list[0]
    pw_list = sd_df['Password'].tolist()#A95G0437
    password = pw_list[0]
    
    users_data = pd.read_csv (r'users.csv')
    
    users_df = pd.DataFrame(users_data, columns= ['Username','Initials'])#A95G0437
    users_list = users_df['Username'].tolist()
    receiver_email = users_list[0]

    settings = {'server': smtp_server,
                'port': port,
                'sender': sender_email,
                'password': password,
                'recipient': receiver_email}
    
    return(settings)

def send_email(settings,text):
    context = ssl.create_default_context()
    print('Sending...')
    with smtplib.SMTP(settings['server'], settings['port']) as server:
        server.starttls(context=context)
        server.login(settings['sender'], settings['password'])
        server.sendmail(settings['sender'], settings['recipient'], text)
        
        print('Sent to {}'.format(settings['recipient']))

#initials = users_df['Initials'].tolist()[0]

#dates,distances,durations,types = dr.data_read(initials)

#date = dates[-1] 
'''
try:
    abbr_data = pd.read_csv(r'temp-abbr.csv')
    abbr_df = pd.DataFrame(abbr_data,columns=['abbr'])
    abbrs = abbr_df['abbr'].tolist()
    ac_abbr = abbrs[0]
    add_animation = False#turned off
except:
    full = dr.pull_data(initials)
    acs = full['Activity number'].tolist()
    
    ac_abbr = acs[-1]
    
    #ac_abbr = 'A95G0437'
    
    add_animation = False
'''

def activity_email(settings,ac_abbr,initials):

    print('Generating email')    

    user_df = dr.pull_data(initials)

    ac_type = dr.activity_details(user_df,ac_abbr,'Type')

    full_date = dr.activity_details(user_df,ac_abbr,'Date')

    date = str(full_date)[:10]
    
    noun,verb,plural = analyse.words(ac_type)
    
    subject = "{} {}".format(noun.capitalize(),date)
    
    message = MIMEMultipart()
    message["From"] = settings['sender']
    message["To"] = settings['recipient']
    message["Subject"] = subject
    
    
    ac_route = analyse.route_data(ac_abbr)
    
    if ac_type != 'Cardio':
        
        #mapper.pyplot_colourmap(ac_route)
    
        mapper.tmb_test(ac_route)
        body = chart_as_html()
    
        #body = add_animation()
    
        body = body + puf.html_assessment(user_df,ac_abbr)
        # body +
        
        puf.activity_comparisons(user_df,ac_abbr)
        body = attach_chart_as_html(body)
    
        #ac_route = analyse.route_data(ac_abbr)
        mapper.pyplot_heatmap(ac_route)
        body = attach_chart_as_html(body)
    
        if ac_type == 'Running':
        
            if dr.activity_details(user_df,ac_abbr,'Distance') > 2414.02/1000:
                puf.times_radar(user_df,ac_abbr)
                body = attach_chart_as_html(body)
        
            if dr.activity_details(user_df,ac_abbr,'Distance') > 1:
                mapper.best_stretch_map_c(ac_abbr,'1km')
        
            if dr.activity_details(user_df,ac_abbr,'Distance') < 4 and dr.activity_details(user_df,ac_abbr,'Distance') > 1:
                body = attach_chart_as_html(body)
                mapper.best_stretch_map(ac_route,1600)
        
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
    
        #analyse.dist_dur_comp(ac_route)
        #body = attach_chart_as_html(body)
    
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
    
        puf.plot_rolling_year_week_progress(user_df,ac_type,date)  
        body = attach_chart_as_html(body)
    
        #ac_df = dr.pull_data(initials)
        puf.plot_week_previous_distances(user_df,date,ac_type)
        #puf.plot_week_and_previous_distances(today_string,ac_type)
        body = attach_chart_as_html(body)
        puf.plot_week_previous_durations(user_df,date,ac_type)
        body = attach_chart_as_html(body)
        puf.plot_month_previous_distances(month,year,ac_type,user_df)#would be nice to redo by date
        body = attach_chart_as_html(body)
    
        puf.plot_distances_equiv_month(user_df,month,year,ac_type)
        body = attach_chart_as_html(body)
        
        if day > 13:###Refers to the wrong Day/Month/Year
            puf.month_calendar(month,year,ac_type,user_df)
            body = attach_chart_as_html(body)
    
        otd_option = puf.otd_list(date,user_df)
        if len(otd_option) > 0:
            body = body + puf.otd_html(date,user_df,img='Y')
    
        #if add_animation == True and ac_type == 'Running':
        #    attach_animation()
    
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
        
        puf.plot_week_previous_durations(user_df,date,ac_type)
        body = attach_chart_as_html(body)
    
        puf.plot_month_and_previous_durations(month,year,ac_type,user_df)
        body = attach_chart_as_html(body)
    
        puf.year_activity_wheel_null(user_df,ac_type,date)
        body = attach_chart_as_html(body)
        puf.year_activity_wheel_null(user_df,'All',date)
        body = attach_chart_as_html(body)
    
        otd_option = puf.otd_list(date,user_df)
        if len(otd_option) > 0:
            body = body + puf.otd_html(date,user_df,img='Y')

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

    send_email(settings, text)
    
def summary_email(settings,initials):
    
    subject = "SNEUE, {} {} {}".format(day,month_caller(month),year)

    message = MIMEMultipart()
    message["From"] = settings['sender']
    message["To"] = settings['recipient']
    message["Subject"] = subject

    #intro = "Maybe one day this will also provide text insights. "
    #message.attach(MIMEText(intro, "plain"))

    body = puf.week_summary_html(y_day_string)
    #message.attach(MIMEText(intro,'html'))
    
    ac_df = dr.pull_data(initials)
    #puf.plot_week_and_previous_distances(y_day_string,'Running')
    puf.plot_week_previous_distances(ac_df,y_day_string,'Running')
    body = attach_chart_as_html(body)  
    #puf.plot_week_and_previous_distances(y_day_string,'Cycling')
    #body = attach_chart_as_html(body)
    #ac_df = dr.pull_data(initials) 
    puf.plot_week_previous_durations(ac_df,y_day_string,'All')
    body = attach_chart_as_html(body)
    
    if day > 13:
        puf.month_calendar(month,year,'All',ac_df)
    
    puf.plot_month_dists(month,year,'Running',ac_df)
    body = attach_chart_as_html(body)
    puf.plot_month_previous_distances(month,year,'Running',ac_df)
    body = attach_chart_as_html(body)
    puf.plot_month_and_previous_durations(month,year,'Running',ac_df)
    body = attach_chart_as_html(body)
    
    #user_df = dr.pull_data(initials)
    puf.plot_distances_equiv_month(ac_df,month,year,'Running')
    body = attach_chart_as_html(body)
    
    if month > 9:
        puf.plot_year_week_progress(ac_df,'Running',year)
    else:
        puf.plot_rolling_year_week_progress(ac_df,'Running',y_day_string) 
    body = attach_chart_as_html(body)

    #puf.plot_month_and_previous_distances(month,year,'Cycling')
    #body = attach_chart_as_html(body)
    puf.plot_month_and_previous_distances(month,year,'Walking',ac_df)
    body = attach_chart_as_html(body)
    puf.plot_distances_this_year(month,year,'Running')
    body = attach_chart_as_html(body)

    puf.year_activity_wheel_null(ac_df,'Running',y_day_string)
    body = attach_chart_as_html(body)
    puf.year_activity_wheel_null(ac_df,'All',y_day_string)
    body = attach_chart_as_html(body)

    puf.plot_cumulative_distance(month,year,'Running')
    body = attach_chart_as_html(body)
    puf.plot_cumulative_distance(month,year,'All')
    body = attach_chart_as_html(body)
    puf.plot_durations_all_previous(month,year,'Running',ac_df)
    body = attach_chart_as_html(body)
    puf.plot_distances_all_previous(month,year,'Running')
    body = attach_chart_as_html(body)   
    
    puf.month_calendar(month,year,'All',ac_df)
    body = attach_chart_as_html(body)

    #muf.plot_month_distances(month,year,'Running')
    #body = attach_chart_as_html(body)
    #muf.plot_distances_this_week(y_day_string,'Running')
    #body = attach_chart_as_html(body)

    outtro = puf.all_personal_bests_html()
    #message.attach(MIMEText(outtro, "html"))

    final = body + outtro

    html = f"""
<html>
{final}
</html>
"""

    message.attach(MIMEText(html,'html'))    

    text = message.as_string()
    
    send_email(settings,text)

ac = dr.latest_activity('WS')

settings = load_settings()

activity_email(settings, ac, 'WS')

#summary_email(settings, 'WS')

