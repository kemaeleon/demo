from django.core.management.base import BaseCommand, CommandError
from abundances.models import TimeCourse
import os, csv
import re
import math

class Command(BaseCommand):
    help = "command to load regulatome data"

    def add_arguments(self, parser):
        parser.add_argument('infile', type=str, help="input file")

    def handle(self, *args, **kwargs):
        os.getcwd()
        all_fields = TimeCourse._meta.get_fields()
        open_fields = [f for f in all_fields if not 
                (re.match(f.name,'id') or re.match("^(Abundance)",  f.verbose_name))] 
        print(open_fields)
        with open(os.path.join(os.getcwd(),kwargs['infile'])) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    e = TimeCourse()
                    for i in open_fields:
                        if re.match("FloatField", e._meta.get_field(i.name).get_internal_type()):
                            setattr(e,i.name,float(row[i.verbose_name]))
                        else:
                            setattr(e,i.name,row[i.verbose_name])  
                         
                    pks = (e.r1, e.r2, e.a1, e.a2, e.m24, e.pos24, e.neg24,
                         e.m48, e.pos48, e.neg48)

                    max_pk = max(pks)

                    def nr(v):
                        return round(v/max_pk,2)

                    def lnr(n,d):
                        return round(Math.log2(n/d),2)

                    e.r1_a = nr(e.r1)
                    e.r2_a = nr(e.r2)
                    e.a1_a = nr(e.a1)
                    e.a2_a = nr(e.a2)
                    e.m24_a = nr(e.m24)
                    e.pos24_a = nr(e.pos24)
                    e.neg24_a = nr(e.neg24)
                    e.m48_a = nr(e.m48)
                    e.pos48_a = nr(e.pos48)
                    e.neg48_a = nr(e.neg48)


                    e.log2_r1a_by_r2a = lnr(e.r1/e.r2)
                    e.log2_a1a_by_a2a = lnr(e.a1/e.a2)
                    e.log2_p24a_by_m24a =  lnr(e.pos24/e.m24)
                    e.log2_n24a_by_m24a =  lnr(e.neg24/e.m24)
                    e.log2_p48a_by_m48a =  lnr(e.pos48/e.m48)
                    e.log2_n48a_by_m48a =  lnr(e.neg48/e.m48)






                    e.save() 
                except:
                    print(row)
                    pass

