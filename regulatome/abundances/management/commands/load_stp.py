from django.core.management.base import BaseCommand, CommandError
from abundances.models import SingleTimePoint
import os, csv
import re



class Command(BaseCommand):
    help = "command to load regulatome data"

    def add_arguments(self, parser):
        parser.add_argument('infile', type=str, help="input file")

    def handle(self, *args, **kwargs):
        os.getcwd()
        all_fields = SingleTimePoint._meta.get_fields()
        print(all_fields)


        with open(os.path.join(os.getcwd(),kwargs['infile'])) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    e = SingleTimePoint()
                    for i in 
                    print(row)
                except:
                    pass
              

