from django.shortcuts import render

from . import htmls
from .GSSutils import data_read as dr
#from .GSSutils import today_string as ts
# Create your views here.

def home(request):
    
    month_previous_running_distances = htmls.month_and_previous_running_distances()
    week_previous_running_distances = htmls.week_and_previous_running_distances()
    
    otd_para = htmls.otd_para()
    
    latest_activity = htmls.latest_activity()
    
    year_week_progress = htmls.year_week_progress()
    
    year_distances = htmls.year_distances()
    
    action_log = htmls.action_log({'page_type': ['home']})
    
    dictionary = {'otd_para': otd_para,
                  'month_prev_run_dist': month_previous_running_distances,
                  'week_prev_run_dist': week_previous_running_distances,
                  'latest_activity': latest_activity,
                  'year_week_progress': year_week_progress,
                  'year_distances': year_distances}
    
    return render(request,'home.html',dictionary)

def index(request):
    
    index_list = htmls.index_list()
    
    action_log = htmls.action_log({'page_type': ['index']})
    
    dictionary = {'index_list' : index_list}
    
    return render(request,'index.html',dictionary)

def activity(request,activity):
    
    route_map = htmls.generate_map(activity,'reg')
    
    radar_plot = htmls.times_radar(activity)
    
    times_table = htmls.times_table(activity)
    
    title = htmls.activity_page_title(activity)
    
    otd = htmls.activity_otd(activity)
    
    action_log = htmls.action_log({'page_type': ['activity'],
                                   'detail': [activity]})
    
    dictionary = {
        'ac_no': activity,
                  'map' : route_map,
                  'type': dr.ac_detail(activity, 'Activity Type'),
                  'distance': dr.ac_detail(activity, 'Distance'),
                  'date': dr.ac_detail(activity, 'Date'),
                  'duration': dr.ac_detail(activity,'Time'),
                  'rankings': htmls.run_rankings_html_str(activity),
                  'times_radar_plot': radar_plot,
                  'title': title,
                  'activity_otd' : otd,
                  'distance_pace': htmls.distance_pace_plot(activity),
                  'comparisons': htmls.comparisons(activity),
                  'times_table': times_table,
                  'times_curve': htmls.times_curve(activity),
                  'prev_post': htmls.prev_post(activity),
                  'shoes': htmls.shoes_activity(activity),
                  'alt_distance_plotly': htmls.pace_alt_plotly(activity),
                  'note': htmls.get_note(activity),
                  'hr_pie': htmls.hr_pie(activity),
                  'hr_dist': htmls.hr_dist(activity),
                  '3D_map': htmls.ThreeD_map(activity),
                  'challenge_update': htmls.challenge_update(activity),
                  'activity_notes': htmls.activity_notes(activity),
                  'km_split_bars': htmls.km_split_bars(activity)
                  }
    
    return render(request, 'activity.html', dictionary)

def activity_two(request,activity):
    
    route_map = htmls.generate_map(activity,'reg')
    
    radar_plot = htmls.times_radar(activity)
    
    times_table = htmls.times_table(activity)
    
    title = htmls.activity_page_title(activity)
    
    otd = htmls.activity_otd(activity)
    
    dictionary = {'ac_no': activity,
                  'map' : route_map,
                  'type': dr.ac_detail(activity, 'Activity Type'),
                  'distance': dr.ac_detail(activity, 'Distance'),
                  'date': dr.ac_detail(activity, 'Date'),
                  'duration': dr.ac_detail(activity,'Time'),
                  'times_radar_plot': radar_plot,
                  'title': title,
                  'activity_otd' : otd,
                  'distance_pace': htmls.distance_pace_plot(activity),
                  'comparisons': htmls.comparisons(activity),
                  'times_table': times_table,
                  'times_curve': htmls.times_curve(activity),
                  'prev_post': htmls.prev_post(activity),
                  'shoes': htmls.shoes_activity(activity),
                  'alt_distance_plotly': htmls.pace_alt_plotly(activity),
                  'note': htmls.get_note(activity),
                  'hr_pie': htmls.hr_pie(activity),
                  'hr_dist': htmls.hr_dist(activity),
                  '3D_map': htmls.ThreeD_map(activity),
                  'challenge_update': htmls.challenge_update(activity)}
    
    return render(request, 'activity2.html', dictionary)

def ac_map(request,activity,distance):
    
    
    
    dictionary = {
        'page_title': htmls.split_page_title(activity, distance, html=False),
        'title': htmls.split_page_title(activity, distance, html=True),
        'reigel_projection': htmls.split_reigel_efficiency(activity, distance),
        'distance_map': htmls.distance_map(activity, distance),
        'km_split_bars': htmls.km_split_bars(activity, distance, whole_activity=False),
        'halfway_split': htmls.halfway_split_p(activity, distance)
                  }
    
    return render(request, 'ac_map.html',dictionary)

def rank_list(request,distance):
    
    dictionary = {'rank_list': htmls.split_rankings(distance),
                  'title': htmls.split_title(distance),
                  'plot': htmls.splits_plotly(distance)#htmls.split_plot(distance)
                  }
    
    action_log = htmls.action_log({'page_type': ['rankings'],
                                   'detail': [distance]})
    
    return render(request, 'split_ranks.html',dictionary)

def rankings_index(request):
    
    dictionary = {'top_set': htmls.top_para(),
                  'splits_plot': htmls.all_splits_plot()}
    
    action_log = htmls.action_log({'page_type': ['rankings'],
                                   'detail': ['index']})
    
    return render(request, 'rankings_index.html',dictionary)

def map_index(request,activity):
    
    dictionary = {'best_times': htmls.map_bt_line(activity)}
    
    return render(request, 'maps.html',dictionary)

def shoes_index(request):
    
    shoes_table = htmls.shoes_table()
    
    action_log = htmls.action_log({'page_type': ['shoes']})
    
    dictionary = {'shoes_table': shoes_table,
                  'shoes_plot': htmls.shoes_plot()}
    
    return render(request, 'shoes.html',dictionary)

def edit_func(request,activity,field,new_string):
    
    edit_complete = htmls.return_edit(activity,field,new_string)
    
    dictionary = {'edit_complete': edit_complete}
    
    return render(request, 'edit_func.html', dictionary)

def edit_index(request,activity):
    
    return render(request,'edit_index.html')
    
def edit_field(request,activity,field):
    
    prompt = htmls.edit_prompt(field)
    
    dictionary = {'prompt': prompt}
    
    return render(request, 'edit_field.html', dictionary)

def challenge_year(request,challenge):
    
    dictionary = {'challenge_title': htmls.challenge_title(challenge),
                  'challenge_summary': htmls.challenge_summary(challenge),
                'challenge_map': htmls.challenge_map(challenge),
                 'challenge_progress': htmls.challenge_progress(challenge),
                 'challenge_table': htmls.challenge_table(challenge)
                 }
    
    action_log = htmls.action_log({'page_type': ['challenge'],
                                   'detail': [challenge]})
    
    return render(request, 'challenge.html',dictionary)

def challenge_index(request):
    
    dictionary = {}
    
    action_log = htmls.action_log({'page_type': ['challenge_index']})
    
    return render(request, 'challenge_index.html',dictionary)

    