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

        gene_ids_tc = [str(i) for i in TimeCourse.objects.all().values_list('gene_id', flat=True)]
        print(len(gene_ids_tc), len(np.unique(gene_ids_tc)))
        gene_ids_sp = [str(i) for i in SingleTimePoint.objects.all().values_list('gene_id', flat=True)]
        gene_ids = np.unique(gene_ids_tc + gene_ids_sp)
        for g in gene_ids:
            print(g)
            list_tc = unpack(TimeCourse.objects.filter(gene_id = g).values_list('id'))
            print(list_tc)
            for c,value in enumerate(list_tc, 1):
                t = TimeCourse.objects.get(pk=value)
                setattr(t,'uniq_gene_id', t.gene_id + "_t_" +  str(c))
                t.save()
            list_sp = unpack(SingleTimePoint.objects.filter(gene_id = g).values_list('id'))
            for c,value in enumerate(list_sp, 1):
                s = SingleTimePoint.objects.get(pk=value)
                setattr(s,'uniq_gene_id', s.gene_id + "_s_" +  str(c))
                s.save()

