"""Views for Regulatome App

This module demonstrates contains definitions of views for
- the front page
- tables, both for single and multitime data sets
- plots
- RESTful API
"""
import json
import random as rd
import re
import string


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django import template
from django.http import HttpResponse
from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2 import RequestConfig, SingleTableMixin
from django_tables2.export.views import ExportMixin
from .models import Gene, MultiTime, SingleTime
from .serializers import MultiTimeSerializer as mts
from .serializers import SingleTimeSerializer as sts
from .filter import GeneFilter, SingleTimeFilter, MultiTimeFilter
from .tables import GeneTable, MultiTimeTable, SingleTimeTable, StatsTable

register = template.Library()

class GeneSearch(SingleTableMixin, FilterView):
    """Search form and filters for the Gene table."""
    model = Gene
    table_class = GeneTable
    filterset_class = GeneFilter
    template_name = "gene_search.html"


class MultiTimeBrowse(ExportMixin, SingleTableMixin, FilterView):
    """Search form and filters for the Multi Time table."""
    model = MultiTime
    table_class = MultiTimeTable
    filterset_class = MultiTimeFilter
    template_name = "multitimebrowse.html"
    extra_content = {'link_to': 'multitimeview'}
    export_formats = ("csv", "xls")


class SingleTimeBrowse(ExportMixin, SingleTableMixin, FilterView):
    """Search form and filters for the Single Time table."""
    model = SingleTime
    table_class = SingleTimeTable
    filterset_class = SingleTimeFilter
    template_name = "singletimebrowse.html"
    extra_content = {'link_to': 'multitimeview'}
    export_formats = ("csv", "xls")


class DV(APIView):
    """Search form and filters for display individual entries
    from the multitime set.
    This is avoids lengthy loading of RESTful data and can be
    useful for demos.
    Not currently used.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """obtain RESTful record for multi time by multi time table primary key"""
        raw = re.search('(?<=rest/multi-time-id-)[a-zA-Z0-9-=_]{2,40}',\
                request.get_full_path())
        multitime_id = raw.group(0)
        data = MultiTime.objects.filter(id=multitime_id).values()[0]
        gene_id = data['gene_id_id']
        data_gene = Gene.objects.filter(id=gene_id).values()[0]
        data_all = {**data, **data_gene}
        return Response(data_all)


def random_color():
    """returns a random hexdec code for a color"""
    lst = [rd.choice(string.hexdigits) for n in range(6)]
    hex_number = "#" + "".join(lst)
    return hex_number


def display_table(request):
    """displays two tables on one page, one for single view, one for multi view"""
    if request.method == "GET":
        pks = request.GET.getlist("selected")
        table_multi = MultiTimeTable(MultiTime.objects.filter(gene_id__in=pks))
        table_single = SingleTimeTable(SingleTime.objects.filter(gene_id__in=pks))
        RequestConfig(request).configure(table_single)
        RequestConfig(request).configure(table_multi)

    return render(request, "bootstrap_template5.html", {
        "table_multi": table_multi, "table_single": table_single

    })


def cross_search(request):
    """form for the search displayed on the front page"""
    search_id = request.GET.getlist("gene_id")
    table_multi = MultiTimeTable(MultiTime.objects.filter(gene_id__gene_id__in=search_id))
    table_single = SingleTimeTable(SingleTime.objects.filter(gene_id__gene_id__in=search_id))
    RequestConfig(request).configure(table_single)
    RequestConfig(request).configure(table_multi)

    return render(request, "cross_search.html", {
        "table_multi": table_multi, "table_single": table_single

    })


def set_uniq_gene_id(single_multi_time):
    """sets uniq gene id"""
    for i in single_multi_time:
        setattr(i, 'uniq_gene_id', i.gene_id.gene_id + "_" + i.gene_id.accession)
        i.save()
    return single_multi_time


def select_tables(pks, single_multi_objects, multi_true):
    """select statistics to display on page"""
    list_tables = []
    for i in pks:
        dt_entry = single_multi_objects.filter(pk=i)
        tid = dt_entry[0].uniq_gene_id
        data_dt_table = None
        if multi_true:
            data_dt_table = MultiTimeTable(dt_entry)
        else:
            data_dt_table = retrieve_stats_table(dt_entry[0])
        data_dt_table.tid = tid
        list_tables.append(data_dt_table)
    return list_tables


def multitimeview(request):
    """function to define tables and plots"""
    type_single = re.search(".*single.*", str(request))
    if request.method == "GET":
        pks = request.GET.getlist("selected")
        if not type_single:
            selected_objects = set_uniq_gene_id(MultiTime.objects.filter(pk__in=pks))
            list_multitables = select_tables(pks, MultiTime.objects, True)
        else:
            selected_objects = set_uniq_gene_id(SingleTime.objects.filter(pk__in=pks))
            list_singletables = select_tables(pks, SingleTime.objects, False)
        selected_objects_list = selected_objects.values()
        context = {}
        if not type_single:
            context['data_tc'] = json.dumps(list(selected_objects_list))
            context['data_stp'] = 0
            context['tablelist'] = list_multitables
            local_template = 'sp_tc2.html'
        else:
            context['data_stp'] = json.dumps(list(selected_objects_list))
            context['data_tc'] = 0
            context['tablelist'] = list_singletables
            local_template = 'sp_tc.html'
    return render(request, local_template, context)



def retrieve_stats_table(single_time):
    """retrieves statistical data for single time point entries"""
    data = [
        {"Ab": "WT/Mock", "log2": single_time.log2_wt_by_mock,\
                "pValue": single_time.p_wt_by_mock, "qValue": single_time.q_wt_by_mock},\
        {"Ab": "\N{GREEK CAPITAL LETTER DELTA}Vif/Mock",\
                "log2": single_time.log2_delta_vif_by_mock,\
                "pValue": single_time.p_delta_vif_by_mock,\
                "qValue": single_time.q_delta_vif_by_mock},\
        {"Ab": "\N{GREEK CAPITAL LETTER DELTA}Vif/WT",\
        "log2": single_time.log2_wt_by_delta_vif, "pValue": single_time.p_wt_by_delta_vif,\
         "qValue": single_time.q_wt_by_delta_vif},

    ]
    stats_table = StatsTable(data)
    return stats_table


class MTView(viewsets.ModelViewSet):
    """RESTful view of single time entries"""
    queryset = MultiTime.objects.all().select_related('gene_id')
    serializer_class = mts


class STView(viewsets.ModelViewSet):
    """RESTful view of time course entries"""
    queryset = SingleTime.objects.all().select_related('gene_id')
    serializer_class = sts


@register.tag(name='update')
def update_variable(value):
    """Allows to update existing variable in template"""
    return value


def announce(request):
    """ variable in template"""
    response = "<html><body><h1>Regulatome@Matheson Lab. coming soon.</h1></body></html>"
    return HttpResponse(response)


def flatten(listoflists):
    """utility function"""
    return [item for liste in listoflists for item in liste]


def homepage(request):
    """hompage view"""
    info = {}
    return render(request, 'index.html', info)


def dicegame(request):
    """dicegame testing django installation"""
    info = {}
    info["no"] = rd.randint(1, 9)
    info["bg"] = random_color()
    info["text"] = random_color()
    return render(request, 'dice.html', info)
