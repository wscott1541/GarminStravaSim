import haversine
import os
import pandas as pd
import time

from math import sqrt
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from . import data_read as dr
from . import loading_modules as lm
    
def nan_to_none(x):
    
    if str(x) == 'nan' or str(x) == 'NONE':
        x = ''
        
    return(x)

def format_url(x):
    
    if 'str' in str(type(x)):
        x = x.replace('_',' ')
        x = x[:1].upper() + x[1:]
        
    return(x)

def reset_distance_column(a_df: pd.DataFrame, include_altitude=False)->List[float]:
    """
    Remeasures distances, including or not including altitude
    NOTE: I'm pretty sure the including altitudes given a misleading distance
    """
    
    distances = [0]
    
    lats = a_df['lat'].tolist()
    lons = a_df['lon'].tolist()
    alts = a_df['alt'].tolist()
    
    
    for i in range(1,len(a_df)):
        prev_lon = lons[i-1]
        prev_lat = lats[i-1]
        prev_alt = alts[i-1]
        
        lon, lat, alt = lons[i], lats[i], alts[i]
        
        delta_2D = haversine.haversine((prev_lat,prev_lon),(lat,lon)) * 1000
        
        if include_altitude:
            delta_alt = alt - prev_alt
                    
            extra_distance = sqrt((delta_2D ** 2) + (delta_alt ** 2))
        else:
            extra_distance = delta_2D
                    
        new = distances[-1] + extra_distance
        
        distances.append(new)
    
    return distances

def recalculate_and_return_best_distances(df: pd.DataFrame, activity_number: str, final_distance: Optional[float] = None)->Tuple[pd.DataFrame, Dict[str, str]]:

    filename = dr.generate_gpx_archive_filename(activity_number)

    if not final_distance:
        final_distance = df['Distance'].tolist()[-1]

    times = {}

    for i in dr.dist_list:
        if final_distance >= dr.dist_dict[i]:
            df = lm.best_time_ws(i, df)
    
            df.to_csv(r'{}'.format(filename))
            print(df.columns)
        
            times[i] = lm.best_time_ws(i, df, True)

    return df, times

def reset_best_times(user_df: pd.DataFrame, activity_number: str, best_times: Dict[str, str])->pd.DataFrame:
    for d in dr.dist_list:
        user_df.loc[user_df['Activity number']==activity_number, d] = best_times.get(d) or 'NONE'
    return user_df

def reset_activity_time(user_df: pd.DataFrame, activity_df: pd.DataFrame, activity_number: str)->pd.DataFrame:
    times = activity_df['time'].tolist()
    
    duration = times[-1] - times[0]

    full_secs = duration.total_seconds()

    user_df.loc[user_df['Activity number']==activity_number, ['Time']] = time.strftime('%H:%M:%S',time.gmtime(full_secs))

    return user_df

def reset_distances(user_df, activity_number, column, new, include_distance=False)->None:
    """
    NOTE: Turning off the distance resetting in favour of just resetting the times
    """
    
    location = user_df.loc[user_df['Activity number'] == activity_number].index.values[0]
    
    filename = dr.generate_gpx_archive_filename(activity_number)
    
    a_df = pd.read_csv(r'{}'.format(filename))
    
    archive = dr.generate_gpx_archive_filename(activity_number+'_a')
    
    a_df.to_csv(archive)
    
    cols = ['time', 'lat', 'lon', 'HR', 'distance', 'cadence', 'alt']
    cols = [c for c in cols if c in list(a_df.columns)]
    a_df = a_df[cols]
    
    if include_distance:
        a_df['distance'] = reset_distance_column(a_df)
    
    final_distance = a_df['distance'].tolist()[-1]
    
    activity = user_df.at[location,'Activity Type']
    
    a_df['time'] = a_df['time'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    
    best_times = {}

    if activity == 'Running':
        a_df, best_times = recalculate_and_return_best_distances(a_df, activity_number, final_distance)
    
    a_df = a_df[cols+list(best_times.keys())]
                
    user_df = reset_best_times(user_df, activity_number, best_times)
        
    user_df.at[location, 'Distance'] = round(final_distance/1000,2)
    
    notes = str(user_df.at[location, 'Notes'])
    a_df.to_csv(r'{}'.format(filename))
    
    if notes == 'nan':
        notes = ''
    else:
        notes = notes+'; '
        
    notes = notes + 'Altered gpx'
    
    user_df.at[location, 'Notes'] = notes
    
    user_df.at[location, 'Date'] = datetime.strftime(a_df['time'].tolist()[0], '%Y-%m-%d %H:%M:%S')
    
    user_df = reset_activity_time(user_df, a_df, activity_number)
    
    user_df.to_csv('activities.csv',index=False)

def remove_activity_from_df(user_df: pd.DataFrame, activity_number: str)->None:
    """
    Removes the database
    Does not remove the activity.csv file
    """

    user_df = user_df[user_df['Activity number'] != activity_number]

    user_df.to_csv('activities.csv',index=False)

def merge_activities(user_df: pd.DataFrame, this_activity: str, activity_to_merge: str, **kwargs)->None:
    """
    Adds records for activity_to_merge to this_activity
    Removes this activity_to_merge from activities df
    Runs best times if appropriate
    """
    archive_name = dr.generate_gpx_archive_filename(this_activity+'_a')
    this_activity_bool = user_df['Activity number'] == this_activity
    to_merge_bool = user_df['Activity number'] == activity_to_merge

    this_activity_df = dr.route_data(this_activity)
    this_activity_filename = dr.generate_gpx_archive_filename(this_activity)
    
    this_activity_df.to_csv(archive_name)

    to_merge = dr.route_data(activity_to_merge)

    df = pd.concat([this_activity_df, to_merge])

    df = df.sort_values(by=['time'], ascending=True)
    
    df['distance'] = df['distance'].diff(periods=1).fillna(0).apply(lambda x: 0 if x<0 else x).cumsum().apply(lambda x: round(x, 2))
    #shift(1).fillna(0)#.cumsum() # from 0->X, 0-Y to 0->X+Y
    # there is no elapsed time equivalent

    if 'alt' in df.columns:
        df['alt'] = df['alt'].fillna(0) 
    # a hack, admittedly, but when I wrote this it was a coastal route that kept returning na

    final_distance = df['distance'].tolist()[-1]

    user_df.loc[this_activity_bool, ['Distance']] = round(final_distance/1000, 2)
    user_df = reset_activity_time(user_df, df, this_activity)

    for measure in ['Rise', 'Fall']:
        this_activity_measure = user_df.loc[this_activity_bool, measure].tolist()[0]
        to_merge_measure = user_df.loc[to_merge_bool, measure].tolist()[0]
        if this_activity_measure != 'NONE' and to_merge_measure != 'NONE':
            if isinstance(this_activity_measure, str):
                this_activity_measure = float(this_activity_measure)
            if isinstance(to_merge_measure, str):
                to_merge_measure = float(to_merge_measure)
            # would be good to convert to the classes with typing

            new_measure = this_activity_measure + to_merge_measure
            new_measure = f'{round(new_measure,1)}'
        else:
            new_measure = 'NONE'
        user_df.loc[this_activity_bool, measure] = new_measure

    activity_type = user_df.loc[this_activity_bool, 'Activity Type'].tolist()[0]

    if activity_type == 'Running':
        df, best_times = recalculate_and_return_best_distances(df, this_activity, final_distance)
        user_df = reset_best_times(user_df, this_activity, best_times)
    else:
        df.to_csv(r'{}'.format(this_activity_filename))

    user_df.to_csv('activities.csv', index=False)

    # remove_activity_from_df(user_df, activity_to_merge)

def download_as_csv(activity_number, suffix):
    
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    
    filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}.csv'.format(activity_number))
    
    a_df = pd.read_csv(r'{}'.format(filename))
    
    def add_csv(x:str)->str:
        return x if x[-4:]=='.csv' else x+'.csv'
    
    if suffix == 'download_csv':
        output_filename = 'activity_' + str(activity_number)
        output_filename = add_csv(output_filename)
    elif suffix  in ['archive', 'original']:
        output_filename = os.path.join(fileDir, 'GPXarchive.gitignore/activity_{}_{}.csv'.format(activity_number, suffix))
    else:
         output_filename = add_csv(suffix)

    a_df.to_csv(r'{}'.format(output_filename))

    return output_filename        

def gen_trkpt(route_data: pd.Series)->str:
    
    time = str(route_data['time']).replace(' ', 'T') + '.000Z'

    if 'alt' in route_data.index:
        elevation = f"<ele>{route_data['alt']}</ele>"
    else:
        elevation = ""
    
    return f'''
<trkpt lat="{route_data['lat']}" lon="{route_data['lon']}">
    {elevation}
    <time>{time}</time>
    <extensions>
        <ns3:TrackPointExtension>
            <ns3:hr>{route_data['HR']}</ns3:hr>
        </ns3:TrackPointExtension>
    </extensions>
</trkpt>'''

def download_as_gpx(activity: dr.Activity)->str:
    s = f'''<?xml version="1.0" encoding="UTF-8"?>
<gpx creator="SOD">
<metadata>
    <time>{activity.date}T{activity.time}.000Z</time>
</metadata>
    <trk>
    <name>{activity.activity_dict["Activity Type"]}</name>
    <type>{activity.activity_dict["Activity Type"].lower()}</type>
    
    <trkseg>
    '''
    
    trkpts = activity.route_data.apply(gen_trkpt, axis=1)
    
    s += '''
'''.join(trkpts.tolist())
    
    s += '''</trkseg>
  </trk>
</gpx>'''

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    
    filename = os.path.join(fileDir, 'activity_{}.gpx'.format(activity.activity_id))

    gpx_file = open(filename, "w")
    n = gpx_file.write(s)
    gpx_file.close()

    return activity.activity_id

def edit_prompt(user_df, column):

    download_as_csv_prompt = """<a href='download_csv'>Download</a> or <a href='archive'>archive</a>
<br>or type the desired filename into the url bar"""
    download_as_gpx_prompt = "<a href='download_gpx'>Download</a>"
    removal_prompt = "If you're sure, <a href='activity_removed'>confirm removal</a>"

    simple_prompt_conversion = {
        'download_csv': download_as_csv_prompt,
        'download_gpx': download_as_gpx_prompt,
        'merge_with': 'Enter id of activity to merge with',
        'Remove': removal_prompt
    }
    
    if column in simple_prompt_conversion:

        text = simple_prompt_conversion[column]

    elif column == 'Shoes':
        
        s_df = user_df[['Date','Shoes']].sort_values(by='Date',ascending=False)
        s_df['Shoes'] = s_df['Shoes'].fillna('NONE')
        s_df = s_df.drop_duplicates(subset=['Shoes'],keep='first')
        shoes = s_df['Shoes'].tolist()
        shoes = list(filter(lambda x: x not in ['NONE', 'default'], shoes))
        shoes = [s for s in shoes if all(b not in s for b in '{}')]
        
        def shoes_link(shoe):
            link = shoe.replace(' ','_')
            return f"<a href='{link}'>{shoe}</a>"
        
        text = '<br>'.join(list(map(shoes_link, shoes))) + '''
<br><br>Remember that dictionaries must be in the form {"Shoes 1": 5.00, "Shoes 2": 5.00} for 5km in Shoes 1
and Shoes 2, with double and not single quotes
'''
    
    else:

        text = 'To amend, add to url with underscores in lieu of spaces'
    
    return text

def edit_field(user_df, activity_number, column, new, activity: dr.Activity):
    """
    Note column is capitalised
    """
    
    location = user_df.loc[user_df['Activity number'] == activity_number].index.values[0]

    edit_fields = ['Notes','Admin','Activity Type','Shoes']#At some point do type, but, for the moment, that contains a space

    column = format_url(column)

    if column in edit_fields:
        
        print(user_df[column].dtype)
        
        if '64' in str(user_df[column].dtype):
            user_df[column] = user_df[column].apply(lambda x: str(x))
        
        user_df[column] = user_df[column].apply(nan_to_none)
        
        new = format_url(new)
        
        user_df.at[location,column] = new
        
        user_df.to_csv('activities.csv', index = False)
        
        out = 'Edit complete'
        
    elif column == 'Reset':
        
        reset_distances(user_df,activity_number,column,new, False)
        
        out = 'File reset'
        
    elif column == 'Download csv':
        
        path = download_as_csv(activity_number,new)
        
        out = 'Downloaded to ' + path
        
    elif column == 'Download gpx':
        path = download_as_gpx(activity)
        
        out = 'GPX downloaded'
    
    elif column == 'Remove':
        remove_activity_from_df(user_df, activity_number)

        out = 'Activity removed'
    elif column == 'Merge with':
        merge_activities(user_df, activity_number, new)
        out = f'{new} activity merged with {activity_number}'
    else:
        out = f'{column} not editable'
        
    return out

    
    