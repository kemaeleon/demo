from django.core.management.base import BaseCommand, CommandError
from abundances.models import Gene,SingleTime,MultiTime
import os, csv
import re
import sys, math

#import routine to match original .csv file headers ("stored as verbose fields in django objects")
class Command(BaseCommand):
    help = "command to load regulatome data"

    def add_arguments(self, parser):
        parser.add_argument('infile', type=str, help="input file")
        parser.add_argument('--type', type=str, help="data type, sp (Single Time Point)  or tc (Time Course)")

    def handle(self, *args, **kwargs):
        os.getcwd()
        input_type = kwargs['type']
        all_fields = []
        if input_type == 'tc':
            all_fields = MultiTime._meta.get_fields()
        elif input_type == 'sp':
            all_fields = SingleTime._meta.get_fields()
        open_fields = [f for f in all_fields if not 
                (re.match(f.name,'id') or re.match("^(Abundance)",  f.verbose_name) or 
                    re.match(f.name, 'gene_id') or re.match(f.name, 'uniq_gene_id'))] 
        with open(os.path.join(os.getcwd(),kwargs['infile'])) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    g = Gene()
                    try:
                        setattr(g,"gene_id", row["Gene ID"])
                        setattr(g,"accession", row["Accession"])
                        setattr(g,"description", row["Description"])
                        setattr(g,"taxonomy", row["Taxonomy"])
                        g.save()
                    except Exception as error_message:
                        print(error_message)
                        g = Gene.objects.get(gene_id = row["Gene ID"], accession=row["Accession"],
                                             description = row["Description"],taxonomy=row["Taxonomy"])    

                    if input_type == 'tc':
                        print("HERE")
                        e = MultiTime()
                        e.gene_id = g
                        print("THERE")
                        for i in open_fields:
                            print("STILL", i.name)
                            if re.match("FloatField", e._meta.get_field(i.name).get_internal_type()):
                                v = float(row[i.verbose_name])
                                if not math.isnan(v): 
                                    setattr(e,i.name,v)
                                else:
                                    setattr(e,i.name,'Null')
                            else:
                                setattr(e,i.name,row[i.verbose_name])  
                        pks = (e.r1, e.r2, e.a1, e.a2, e.m24, e.pos24, e.neg24,
                         e.m48, e.pos48, e.neg48)
                        max_pk = max(pks)
                        print("HHHH")

                        def nr(av):
                            return round(av/max_pk,2)
                        def lnr(n,d):
                            return round(math.log2(n/d),2)

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
                        
                        e.log2_r1a_by_r2a = lnr(e.r1,e.r2)
                        e.log2_a1a_by_a2a = lnr(e.a1,e.a2)
                        e.log2_p24a_by_m24a =  lnr(e.pos24,e.m24)
                        e.log2_n24a_by_m24a =  lnr(e.neg24,e.m24)
                        e.log2_p48a_by_m48a =  lnr(e.pos48,e.m48)
                        e.log2_n48a_by_m48a =  lnr(e.neg48,e.m48)

                        e.save() 
                        print("PASSEDSAVE")
                    elif input_type == 'sp':
                        e = SingleTime()
                        e.gene_id = g
                        for i in open_fields:
                            if re.match("FloatField", e._meta.get_field(i.name).get_internal_type()):
                                v = float(row[i.verbose_name])
                                if not math.isnan(v):
                                    setattr(e,i.name,v)
                                else:
                                    setattr(e,i.name,'Null')
                            else:
                                setattr(e,i.name,row[i.verbose_name])  
                        sp_peak = (e.a_mock, e.b_mock, e.c_mock, e.a_wt, e.b_wt, e.c_wt, e.a_delta_vif, e.b_delta_vif, e.c_delta_vif)
                        sp_max_pk = max(sp_peak)
                        def sp_nr(av):
                            print("HOHOHO", round(av/sp_max_pk,2))
                            return round(av/sp_max_pk,2)

                        e.a_a_mock = sp_nr(e.a_mock) 
                        e.a_b_mock = sp_nr(e.b_mock)
                        e.a_c_mock = sp_nr(e.c_mock)
                        e.a_a_wt = sp_nr(e.a_wt)
                        e.a_b_wt = sp_nr(e.b_wt)
                        e.a_c_wt = sp_nr(e.c_wt)
                        e.a_a_delta_vif = sp_nr(e.a_delta_vif) 
                        e.a_b_delta_vif = sp_nr(e.b_delta_vif)
                        e.a_c_delta_vif = sp_nr(e.c_delta_vif)

                        e.log2_wt_by_mock = round(e.log2_wt_by_mock,2)
                        e.p_wt_by_mock = round(e.p_wt_by_mock,5)
                        e.q_wt_by_mock = round(e.q_wt_by_mock,5)
                        e.log2_delta_vif_by_mock = round(e.log2_delta_vif_by_mock,2) 
                        e.p_delta_vif_by_mock = round(e.p_delta_vif_by_mock,5)
                        e.q_delta_vif_by_mock = round(e.q_delta_vif_by_mock,5) 
                        e.log2_wt_by_delta_vif = round(e.log2_wt_by_delta_vif,2)
                        e.p_wt_by_delta_vif =  round(e.p_wt_by_delta_vif,5)
                        e.q_wt_by_delta_vif = round(e.q_wt_by_delta_vif,5)
                        e.save()    

                except Exception as error_message:
                    print(error_message)
                     
                 

