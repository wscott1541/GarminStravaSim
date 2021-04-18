"""GGSsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from GSS import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index,name='index'),
    path('', views.home, name='home'),
    path('index/<activity>/',views.activity,name='<activity>'),
    path('rankings/<distance>',views.rank_list,name='<distance>_rankings'),
    path('rankings/',views.rankings_index,name='rankings'),
    path('index/<activity>/map/<distance>/',views.ac_map,name='<activity>_<distance>_map'),
    path('index/<activity>/map/', views.map_index, name='<activity>_maps'),
    path('shoes/', views.shoes_index, name='shoes'),
    path('index/<activity>/edit/<field>/<new_string>/', views.edit_func, name='<activity>_<field>_edit_func'),
    path('index/<activity>/edit/', views.edit_index, name='<activity>_edit'),
    path('index/<activity>/edit/<field>/',views.edit_field, name = '<activity>_edit_<field>'),
    path('challenges/<challenge>/',views.challenge_year,name='<challenge>')
    
]

"""

SITE MAP THOUGHTS

/rank/<distance>: a list of distance split rankings

index/activity/dist_map/<distance>
index/activity/cust_map/<distance>  could combine these
index/activty/lap/<n> map for specific laps (can link to 1,2,3,4,5 etc)
index/activity/edit : index of editable options
index/activity/edit/field : input of editable options
index/activity/edit/field/new_string : creates edit based on url?

index/activity/load/<func>
- email
- altitude (if not found)

/shoes Could definitely do a nice graph for this

/summary/year/ac_type (Would this work for 'all'?)
/summary/all_time/ac_type
/summary/month/

summary/.../ email?

"""
