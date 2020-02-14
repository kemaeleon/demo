from django.conf.urls import url
from django.views import debug
from django.contrib import admin
from abundances import views, models
from abundances.models import TimeCourse
from abundances.views import DV,FilterListView,OverView,SingleTimePointListView 

urlpatterns = [
    url(r'^dice$', views.dicegame, name='dice'),
    url(r'results_timecourse', views.someview),
    url(r'results_singletimepoint', views.singletimepointview),
    url(r'mouse', views.redirectindex),
    url(r'resultindex[a-zA-Z0-9-=_]',views.indexview),
    url(r'^db$', FilterListView.as_view(), name="filtertableview"), # search interface
    url(r'^dbsp$', SingleTimePointListView.as_view(), name="singletimepointlistview"), # search interface
    url(r'^indexview2$', OverView.as_view(), name="indexview2"), # search interface
    url(r'^rest/uniq-gene-id-[a-zA-Z0-9-=_]{2,40}$', DV.as_view()), # RESTful data view
   # url('', debug.default_urlconf)
    url('', views.announce)
]

