"""url module """
from django.conf.urls import url
from django.views import debug
from abundances import views
from abundances.views import  MTView, STView


urlpatterns = [
    url(r'^dicegame$', views.dicegame, name='dice'),
    url(r'^home$', views.homepage, name='home'),
    url(r'^gene_search$', views.GeneSearch.as_view(), name='gene_search'),
    url(r'^plot_multi', views.multitimeview, name = 'multitimeplot'),
    url(r'^plot_single', views.multitimeview, name = 'singletimeplot'),
    url(r'^example', views.cross_search, name = 'cross_search'),
    url(r'^results_tables', views.display_table, name='tables_view'),
    url(r'^multitime_browse', views.MultiTimeBrowse.as_view(), name='multitime_browse'),
    url(r'^singletime_browse', views.SingleTimeBrowse.as_view(), name='singletime_browse'),
    url(r'^rest/multi-time-id-[a-zA-Z0-9-=_]{2,40}$', views.DV.as_view()),
    url(r'^rest/MT', MTView.as_view({'get': 'list'}), name='multitime_restful'),
    url(r'^rest/ST', STView.as_view({'get': 'list'}), name='singletime_restful'),
    url('', debug.default_urlconf)
    # url('', views.announce)
]
