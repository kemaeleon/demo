from django.conf.urls import url
from django.views import debug
from django.contrib import admin
from abundances import views, models
from abundances.models import TimeCourse
from abundances.views import DV,GeneSearch,MTView,STView

urlpatterns = [
    url(r'^dice$', views.dicegame, name='dice'),
    url(r'^home$', views.homepage, name='home'),
    url(r'^gene_search$', views.GeneSearch.as_view(), name='gene_search'),
    url(r'plot_[a-z]{4,40}time', views.multitimeview),
    url(r'example', views.hackview),
    url(r'results_tables', views.display_table, name='tables_view'),
    url(r'multitime_browse',views.MultiTimeBrowse.as_view(), name='multitime_browse'),
    url(r'singletime_browse', views.SingleTimeBrowse.as_view(), name='singletime_browse'),
    url(r'^rest/multi-time-id-[a-zA-Z0-9-=_]{2,40}$', DV.as_view()), # RESTful data view
    url(r'^rest/MT', MTView.as_view({'get': 'list'}), name="multitime_restful"), # RESTful data view
    url(r'^rest/ST', STView.as_view({'get': 'list'}), name="singletime_restful"), # RESTful data view

   # url('', debug.default_urlconf)
    url('', views.announce)
]

