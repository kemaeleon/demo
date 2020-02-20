from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import re
import random as rd, string
from abundances.models import TimeCourse,IndexAbundance,SingleTimePoint,Gene,MultiTime
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse
from django.core import serializers
from random import choice

from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.lorem_ipsum import words
from django.views.generic.base import TemplateView
from django_filters.views import FilterView

from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
from django_tables2.paginators import LazyPaginator
from .tables import PeakTable, IndexTable, SingleTimePointTable, GeneTable, MultiTimeTable
from .filter import TimeCourseFilter, SingleTimePointFilter, IndexFilter, GeneFilter,Gene, MultiTimeFilter
from django.http import JsonResponse
from django.shortcuts import redirect


class GeneSearch(ExportMixin, SingleTableMixin, FilterView):
    model = Gene
    table_class = GeneTable
    filterset_class = GeneFilter
    template_name = "bootstrap_template4.html"

    export_formats = ("csv", "xls")

    def get_queryset(self):
        return super().get_queryset()

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}



class FilterListView(ExportMixin, SingleTableMixin, FilterView):
    model = TimeCourse
    table_class = PeakTable
    filterset_class = TimeCourseFilter
    template_name = "bootstrap_template.html"

    export_formats = ("csv", "xls")

    def get_queryset(self):
        return super().get_queryset()

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}

class SingleTimePointListView(ExportMixin, SingleTableMixin, FilterView):
    model = SingleTimePoint
    table_class = SingleTimePointTable 
    filterset_class = SingleTimePointFilter
    template_name = "bootstrap_template_sp.html"

    export_formats = ("csv", "xls")

    def get_queryset(self):
        return super().get_queryset()

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}



class OverView(ExportMixin, SingleTableMixin,FilterView):
    model = IndexAbundance
    table_class = IndexTable
    filterset_class = IndexFilter
    template_name = "bootstrap_template2.html"

    def get_queryset(self):
        return super().get_queryset()
    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}


class DV(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        raw = re.search('(?<=rest/uniq-gene-id-)[a-zA-Z0-9-=_]{2,40}', request.get_full_path())
        gene_id = raw.group(0)
        df = pd.DataFrame(TimeCourse.objects.filter(uniq_gene_id=gene_id).values())
        if len(df) == 0:
           df = pd.DataFrame(SingleTimePoint.objects.filter(uniq_gene_id=gene_id).values())
        return Response(df)


def random_color():
    lst = [rd.choice(string.hexdigits) for n in range(6)]
    hex_number = "#" +  "".join(lst)
    return hex_number



class TableResultView(ExportMixin, SingleTableMixin, FilterView):
        table_class = MultiTimeTable
        filterset_class = MultiTimeFilter
        template_name = "bootstrap_template.html"

        export_formats = ("csv", "xls")

        def get_queryset(self):
            return super().get_queryset()

        def get_table_kwargs(self):
            return {"template_name": "django_tables2/bootstrap.html"}



def display_table(request):
    if request.method == "POST":
        pks = request.POST.getlist("selected")
        print("pks", pks)
        table_multi = MultiTimeTable(MultiTime.objects.filter(gene_id__in=pks))

    def get_table_kwargs(table):
        return {"template_name": "django_tables2/bootstrap.html"}

    return render(request, "bootstrap_template5.html", {
        "table": table_multi
    })






def timecourseview(request):
    if request.method == "POST":
        pks = request.POST.getlist("selected")
        selected_objects = TimeCourse.objects.filter(pk__in=pks).values()
        selected_geneids = TimeCourse.objects.filter(pk__in=pks).values_list('uniq_gene_id',flat=True)
        context = {}
        context['uniq_gene_id'] = list(selected_geneids)
        context['data_tc'] = json.dumps(list(selected_objects))
        context['data_stp'] = None
    return render(request, 'sp_tc.html', context)


def singletimepointview(request):
    if request.method == "POST":
        pks = request.POST.getlist("selected")
        selected_objects = SingleTimePoint.objects.filter(pk__in=pks).values()
        selected_geneids = SingleTimePoint.objects.filter(pk__in=pks).values_list('uniq_gene_id',flat=True)
        context = {}
        context['uniq_gene_id'] = list(selected_geneids)
        context['data_stp'] = json.dumps(list(selected_objects))
    return render(request, 'singletimepoint.html', context)

def announce(request):
    response = "<html><body><h1>Regulatome@Matheson Lab. coming soon.</h1></body></html>"
    return HttpResponse(response)


def redirectindex(request):
    if request.method == "POST":
        pks=request.POST.getlist("selected")
        label = ['resultindex']
        newurl = '/' + '_'.join(label+pks) + '/'
        response = redirect(newurl)
        return response

def flatten(listoflists):
    return [item for liste in listoflists for item in liste]

def indexview(request):
    if request != "":
        # obtain IndexAbundance primary keys from URL
        pks = [int(i) for i in re.split('/|_', str(request.get_full_path())) if i.isdigit() ]
        # obtain pks of TimeCourse and SingleTimePoint objects 
        
        # get time course data
        tc = [i['time_course'] for i in list(IndexAbundance.objects.filter(pk__in=pks).values('time_course'))]
        l2 = flatten(tc)
        sel_timecourse = TimeCourse.objects.filter(pk__in=l2).values() 
        selected_gene_tc = TimeCourse.objects.filter(pk__in=l2).values_list('uniq_gene_id', flat=True)

        # get single point data
        selected_sp =[i['single_time_point'] for i in list(IndexAbundance.objects.filter(pk__in=pks).values('single_time_point'))]
        l2 = flatten(selected_sp)
        sel_stp = SingleTimePoint.objects.filter(pk__in=l2).values() 
        selected_gene_spt = SingleTimePoint.objects.filter(pk__in=l2).values_list('uniq_gene_id', flat=True)

        selected_geneids = list(selected_gene_tc) + list(selected_gene_spt)
        selected_geneids.sort()
       
        context = {}
        context['uniq_gene_id'] = selected_geneids
        context['data_tc'] = json.dumps(list(sel_timecourse))
        context['data_stp'] = json.dumps(list(sel_stp))
    return render(request, 'sp_tc.html', context)



def dicegame(request):
    info = {}
    info["no"] = rd.randint(1,9)
    info["bg"]= random_color()
    info["text"] = random_color()
    return render(request, 'dice.html',info)
