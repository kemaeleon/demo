from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
import pandas as pd
import re
import random as rd, string
from abundances.models import Gene,MultiTime,SingleTime
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse
from django.core import serializers
from random import choice
from abundances.serializers import GeneSerializer as gs
from abundances.serializers import MultiTimeSerializer as mts
from abundances.serializers import SingleTimeSerializer as sts
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.lorem_ipsum import words
from django.views.generic.base import TemplateView
from django_filters.views import FilterView

from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
from django_tables2.paginators import LazyPaginator
from .tables import  GeneTable, MultiTimeTable, SingleTimeTable
from .filter import GeneFilter,SingleTimeFilter,MultiTimeFilter
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

class MultiTimeBrowse(ExportMixin, SingleTableMixin, FilterView):
    model = MultiTime 
    table_class = MultiTimeTable
    filterset_class = MultiTimeFilter
    template_name = "bootstrap_template6.html"

    export_formats = ("csv", "xls")

    def get_queryset(self):
        return super().get_queryset()

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}

class SingleTimeBrowse(ExportMixin, SingleTableMixin, FilterView):
    model = Gene
    table_class = GeneTable
    filterset_class = GeneFilter
    template_name = "bootstrap_template6.html"

    export_formats = ("csv", "xls")

    def get_queryset(self):
        return super().get_queryset()

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}



class DV(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        raw = re.search('(?<=rest/multi-time-id-)[a-zA-Z0-9-=_]{2,40}', request.get_full_path())
        multitime_id = raw.group(0)
        data = MultiTime.objects.filter(id=multitime_id).values()[0]
        print(data['gene_id_id'])
        gene_id = data['gene_id_id']
        data_gene =  Gene.objects.filter(id=gene_id).values()[0]
        data_all = {**data, **data_gene}
        return Response(data_all)


def random_color():
    lst = [rd.choice(string.hexdigits) for n in range(6)]
    hex_number = "#" +  "".join(lst)
    return hex_number



def display_table(request):
    if request.method == "GET":
        pks = request.GET.getlist("selected")
        print("pks", pks)
        table_multi = MultiTimeTable(MultiTime.objects.filter(gene_id__in=pks))
        table_single = SingleTimeTable(SingleTime.objects.filter(gene_id__in=pks))

    def get_table_kwargs(table):
        return {"template_name": "django_tables2/bootstrap.html"}

    return render(request, "bootstrap_template5.html", {
        "table_multi": table_multi, "table_single": table_single

    })


def hackview(request):
    search_id = request.POST.getlist("gene_id")
    selected_objects_t = MultiTime.objects.filter(gene_id__gene_id__in=search_id)
    selected_objects_s = SingleTime.objects.filter(gene_id__gene_id__in=search_id)
    for i in selected_objects_t:
            setattr(i, 'uniq_gene_id', i.gene_id.gene_id + "_" +  i.gene_id.accession + "_t")
            i.save()
    for i in selected_objects_s:
            setattr(i, 'uniq_gene_id', i.gene_id.gene_id + "_" +  i.gene_id.accession + "_s")
            i.save()        
    selected_objects_list_t = selected_objects_t.values()
    selected_objects_list_s = selected_objects_s.values()
    selected_geneids_t  = selected_objects_t.values_list('uniq_gene_id',flat=True)
    selected_geneids_s = selected_objects_s.values_list('uniq_gene_id',flat=True)
    selected_geneids = list(selected_geneids_t) + list(selected_geneids_s)
    context = {}
    context['uniq_gene_id'] = selected_geneids
    context['data_tc'] = json.dumps(list(selected_objects_list_t))   
    context['data_stp'] = json.dumps(list(selected_objects_list_s))
    return render(request, 'sp_tc.html', context)


def multitimeview(request):
    print(request.GET.getlist("gene_id"))
    x = re.search(".*multi.*", str(request))
    multi = False
    if (x):
        multi = True
    if request.method == "GET":
        pks = request.GET.getlist("selected")
        selected_obects = None
        if multi is True:
            selected_objects = MultiTime.objects.filter(pk__in=pks)
        else:
            selected_objects = SingleTime.objects.filter(pk__in=pks)
        for i in selected_objects:
            setattr(i, 'uniq_gene_id', i.gene_id.gene_id + "_" +  i.gene_id.accession)
            i.save()
        selected_objects_list = selected_objects.values()
        selected_geneids = selected_objects.values_list('uniq_gene_id',flat=True)    
        context = {}
        context['uniq_gene_id'] = list(selected_geneids) 
        if multi is True:
            context['data_tc'] = json.dumps(list(selected_objects_list))
            context['data_stp'] = 0
        else:
            context['data_stp'] = json.dumps(list(selected_objects_list))
            print(context['data_stp'])
            context['data_tc'] = 0

    return render(request, 'sp_tc.html', context)


class MTView(viewsets.ModelViewSet):
    queryset = MultiTime.objects.all().select_related('gene_id')
    serializer_class = mts

class STView(viewsets.ModelViewSet):
    queryset = SingleTime.objects.all().select_related('gene_id')
    serializer_class = sts




def announce(request):
    response = "<html><body><h1>Regulatome@Matheson Lab. coming soon.</h1></body></html>"
    return HttpResponse(response)


def flatten(listoflists):
    return [item for liste in listoflists for item in liste]

def homepage(request):
    info = {}
    return render(request, 'index.html',info) 

def dicegame(request):
    info = {}
    info["no"] = rd.randint(1,9)
    info["bg"]= random_color()
    info["text"] = random_color()
    return render(request, 'dice.html',info)
