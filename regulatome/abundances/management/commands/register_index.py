from django.core.management.base import BaseCommand, CommandError
from abundances.models import TimeCourse,SingleTimePoint, IndexAbundance
import os, csv
import re
import numpy as np

class Command(BaseCommand):
    help = "command to load register indices timecourse data"


    def handle(self, *args, **kwargs):
        def unpack(tuplelist):
            return [item for t in list(tuplelist) for item in t]
        IndexAbundance.objects.all().delete()
        gene_ids_tc = [str(i) for i in TimeCourse.objects.all().values_list('gene_id', flat=True)]
        print(len(gene_ids_tc), len(np.unique(gene_ids_tc)))
        gene_ids_sp = [str(i) for i in SingleTimePoint.objects.all().values_list('gene_id', flat=True)]
        gene_ids = np.unique(gene_ids_tc + gene_ids_sp)
        for g in gene_ids:
            ttoken = ""
            list_tc = unpack(TimeCourse.objects.filter(gene_id = g).values_list('id'))
            for c,value in enumerate(list_tc, 1):
                ttoken += "O"
                t = TimeCourse.objects.get(pk=value)
                setattr(t,'uniq_gene_id', t.gene_id + "_" + str(c))
            list_sp = unpack(SingleTimePoint.objects.filter(gene_id = g).values_list('id'))
            stoken = ""
            for c,value in enumerate(list_sp, 1):
                stoken += "O"
                s = SingleTimePoint.objects.get(pk=value)
                setattr(t,'uniq_gene_id', s.gene_id + "_" + str(c))
            i = IndexAbundance.objects.create(gene_id = g, time_course = list_tc,
                                            single_time_point = list_sp, time_course_tokens = ttoken, single_time_tokens = stoken)
            i.save()
