from django.core.management.base import BaseCommand, CommandError
from abundances.models import TimeCourse,SingleTimePoint, IndexAbundance
import os, csv
import re
import numpy as np
from django.db.models import Count

class Command(BaseCommand):
    help = "command to load register indices timecourse data"


    def handle(self, *args, **kwargs):
        duplicates = TimeCourse.objects.values('gene_id').annotate(name_count=Count('gene_id')).filter(name_count__gt=1)
        print(duplicates)
        records = TimeCourse.objects.filter(gene_id__in=[item['gene_id'] for item in duplicates])
        print(records)
        print([item.id for item in records])


