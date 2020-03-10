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


class GeneSearch(ExportMixin, SingleTableMixin, FilterView):
    model = Gene
    table_class = GeneTable
    filterset_class = GeneFilter
    template_name = "bootstrap_template4.html"
    export_formats = ()


class MultiTimeBrowse(ExportMixin, SingleTableMixin, FilterView):
    model = MultiTime
    table_class = MultiTimeTable
    filterset_class = MultiTimeFilter
    template_name = "bootstrap_template6.html"
    export_formats = ("csv", "xls")

class SingleTimeBrowse(ExportMixin, SingleTableMixin, FilterView):
    model = SingleTime
    table_class = SingleTimeTable
    filterset_class = SingleTimeFilter
    template_name = "bootstrap_template7.html"

    export_formats = ("csv", "xls")


class DV(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        raw = re.search('(?<=rest/multi-time-id-)[a-zA-Z0-9-=_]{2,40}', request.get_full_path())
        multitime_id = raw.group(0)
        data = MultiTime.objects.filter(id=multitime_id).values()[0]
        gene_id = data['gene_id_id']
        data_gene = Gene.objects.filter(id=gene_id).values()[0]
        data_all = {**data, **data_gene}
        return Response(data_all)


def random_color():
    lst = [rd.choice(string.hexdigits) for n in range(6)]
    hex_number = "#" + "".join(lst)
    return hex_number


def display_table(request):
    if request.method == "GET":
        pks = request.GET.getlist("selected")
        table_multi = MultiTimeTable(MultiTime.objects.filter(gene_id__in=pks))
        table_single = SingleTimeTable(SingleTime.objects.filter(gene_id__in=pks))
        RequestConfig(request).configure(table_single)
        RequestConfig(request).configure(table_multi)

    def get_table_kwargs(table):
        return {"template_name": "django_tables2/bootstrap.html"}

    return render(request, "bootstrap_template5.html", {
        "table_multi": table_multi, "table_single": table_single

    })


def simplesearch(request):
    search_id = request.GET.getlist("gene_id")
    table_multi = MultiTimeTable(MultiTime.objects.filter(gene_id__gene_id__in=search_id))
    table_single = SingleTimeTable(SingleTime.objects.filter(gene_id__gene_id__in=search_id))
    RequestConfig(request).configure(table_single)
    RequestConfig(request).configure(table_multi)

    def get_table_kwargs(table):
        return {"template_name": "django_tables2/bootstrap.html"}

    return render(request, "bootstrap_template5.html", {
        "table_multi": table_multi, "table_single": table_single

    })



def multitimeview(request):
    template = ''
    list_singletables = []
    list_multitables = []
    x = re.search(".*single.*", str(request))
    multi = True
    if x:
        multi = False
    if request.method == "GET":
        pks = request.GET.getlist("selected")
        selected_obects = None
        if multi is True:
            selected_objects = MultiTime.objects.filter(pk__in=pks)
            for i in selected_objects:
                setattr(i, 'uniq_gene_id', i.gene_id.gene_id + "_" + i.gene_id.accession)
                i.save()
            for primkey in pks:
                multi_dt_entry = MultiTime.objects.filter(pk=primkey)
                tid = multi_dt_entry[0].uniq_gene_id
                multi_dt_table = MultiTimeTable(multi_dt_entry)
                multi_dt_table.tid = tid
                list_multitables.append(multi_dt_table)
        else:
            selected_objects = SingleTime.objects.filter(pk__in=pks)
            for i in selected_objects:
                setattr(i, 'uniq_gene_id', i.gene_id.gene_id + "_" + i.gene_id.accession)
                i.save()
            for primkey in pks:
                single_dt_entry = SingleTime.objects.filter(pk=primkey)
                tid = single_dt_entry[0].uniq_gene_id
                single_dt_table = retrieveStatsTable2(single_dt_entry[0])
                single_dt_table.tid = tid
                list_singletables.append(single_dt_table)
        for i in selected_objects:
            setattr(i, 'uniq_gene_id', i.gene_id.gene_id + "_" + i.gene_id.accession)
            i.save()
        selected_objects_list = selected_objects.values()
        selected_geneids = selected_objects.values_list('uniq_gene_id', flat=True)
        table_single = SingleTimeTable(SingleTime.objects.filter(gene_id__gene_id__in=['Gagpol', ]))
        context = {}
        context['uniq_gene_id'] = list(selected_geneids)
        if multi is True:
            context['data_tc'] = json.dumps(list(selected_objects_list))
            context['data_stp'] = 0
            context['tablelist'] = list_multitables
            template = 'sp_tc2.html'
        else:
            context['data_stp'] = json.dumps(list(selected_objects_list))
            context['data_tc'] = 0
            context['tablelist'] = list_singletables
            template = 'sp_tc.html'
        context['table'] = list_singletables
    return render(request, template, context)


def retrieveStatsTable():
    data = [
        {"d": "WT/Mock", "v": "100", "p_val": "10", "q": "20"},
        {"d": "\N{GREEK CAPITAL LETTER DELTA}Vif/Mock", "v": "300", "p_val": "20", "q": "30"},
        {"d": "\N{GREEK CAPITAL LETTER DELTA}Vif/WT", "v": "499", "p_val": "10", "q": "20"},

    ]
    stats_table = StatsTable(data)
    return stats_table


def retrieveStatsTable2(st):
    data = [
        {"Ab": "WT/Mock", "log2": st.log2_wt_by_mock,
                "pValue": st.p_wt_by_mock, "qValue": st.q_wt_by_mock},
        {"Ab": "\N{GREEK CAPITAL LETTER DELTA}Vif/Mock",
                "log2": st.log2_delta_vif_by_mock,
         "pValue": st.p_delta_vif_by_mock, "qValue": st.q_delta_vif_by_mock},
        {"Ab": "\N{GREEK CAPITAL LETTER DELTA}Vif/WT",
                "log2": st.log2_wt_by_delta_vif, "pValue": st.p_wt_by_delta_vif,
         "qValue": st.q_wt_by_delta_vif},

    ]
    stats_table = StatsTable(data)
    return stats_table


class MTView(viewsets.ModelViewSet):
    queryset = MultiTime.objects.all().select_related('gene_id')
    serializer_class = mts


class STView(viewsets.ModelViewSet):
    queryset = SingleTime.objects.all().select_related('gene_id')
    serializer_class = sts


@register.tag(name='update')
def update_variable(value):
    """Allows to update existing variable in template"""
    return value


def announce(request):
    response = "<html><body><h1>Regulatome@Matheson Lab. coming soon.</h1></body></html>"
    return HttpResponse(response)


def flatten(listoflists):
    return [item for liste in listoflists for item in liste]


def homepage(request):
    info = {}
    return render(request, 'index.html', info)


def dicegame(request):
    info = {}
    info["no"] = rd.randint(1, 9)
    info["bg"] = random_color()
    info["text"] = random_color()
    return render(request, 'dice.html', info)
