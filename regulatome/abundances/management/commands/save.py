"""command to load regulatome data into django from spreadsheets"""
import os
import re
import math
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from abundances.models import Gene, SingleTime, MultiTime


def peak_to_ab(peak, max_pk):
    """converting absolute protein expression to protein abundances"""
    return round(peak / max_pk, 2)


def log_ab(peak, control):
    """log2 of protein expression ration"""
    return round(math.log2(peak / control), 2)


def populate_gene(row):
    """filling gene object with protein information data"""
    try:
        gene = Gene()
        try:
            setattr(gene, "gene_id", row["Gene ID"])
            setattr(gene, "accession", row["Accession"])
            setattr(gene, "description", row["Description"])
            setattr(gene, "taxonomy", row["Taxonomy"])
            gene.save()
        except ObjectDoesNotExist as error_message:
            gene = Gene.objects.get(gene_id=row["Gene ID"],
                                    accession=row["Accession"],
                                    description=row["Description"],
                                    taxonomy=row["Taxonomy"])
    except Exception as error_message:
        print("UGLYOWN")
        print(error_message)
    return gene

def populate_multi_time(row, required_fields, gene):
    """filling multi time object with protein expression data"""
    try:
        entry = MultiTime()
        try:
            entry.gene_id = gene
            print("CARAMBA" + gene)
            entry.save()
        except Exception as error_message:
            print(error_message)
        for i in required_fields:
            if re.match("FloatField",
                        entry._meta.get_field(i.name).get_internal_type()):
                peak_value = float(row[i.verbose_name])
                if not math.isnan(peak_value):
                    setattr(entry, i.name, peak_value)
                else:
                    setattr(entry, i.name, 'Null')
            else:
                setattr(entry, i.name, row[i.verbose_name])
        pks = (entry.r1, entry.r2, entry.a1, entry.a2,
               entry.m24, entry.pos24, entry.neg24,
               entry.m48, entry.pos48, entry.neg48)
        max_pk = max(pks)


        entry.r1_a = peak_to_ab(entry.r1, max_pk)
        entry.r2_a = peak_to_ab(entry.r2, max_pk)
        entry.a1_a = peak_to_ab(entry.a1, max_pk)
        entry.a2_a = peak_to_ab(entry.a2, max_pk)
        entry.m24_a = peak_to_ab(entry.m24, max_pk)
        entry.pos24_a = peak_to_ab(entry.pos24, max_pk)
        entry.neg24_a = peak_to_ab(entry.neg24, max_pk)
        entry.m48_a = peak_to_ab(entry.m48, max_pk)
        entry.pos48_a = peak_to_ab(entry.pos48, max_pk)
        entry.neg48_a = peak_to_ab(entry.neg48, max_pk)
        entry.log2_r1a_by_r2a = log_ab(entry.r1, entry.r2)
        entry.log2_a1a_by_a2a = log_ab(entry.a1, entry.a2)
        entry.log2_p24a_by_m24a = log_ab(entry.pos24, entry.m24)
        entry.log2_n24a_by_m24a = log_ab(entry.neg24, entry.m24)
        entry.log2_p48a_by_m48a = log_ab(entry.pos48, entry.m48)
        entry.log2_n48a_by_m48a = log_ab(entry.neg48, entry.m48)
        entry.save()
    except Exception as error_message:
        print(error_message)


def populate_single_time(row, required_fields, gene):
    """filling single time object with protein expression data"""
    try:
        entry = SingleTime()
        entry.gene_id = gene
        for i in required_fields:
            if re.match("FloatField", \
                entry._meta.get_field(i.name).get_internal_type()):
                peak_val = float(row[i.verbose_name])
                if not math.isnan(peak_val):
                    setattr(entry, i.name, peak_val)
                else:
                    setattr(entry, i.name, 'Null')
            else:
                setattr(entry, i.name, row[i.verbose_name])
        sp_peak = (entry.a_mock, entry.b_mock, entry.c_mock,
                   entry.a_wt, entry.b_wt, entry.c_wt,
                   entry.a_delta_vif, entry.b_delta_vif,
                   entry.c_delta_vif)
        sp_max_pk = max(sp_peak)

        entry.a_a_mock = peak_to_ab(entry.a_mock, sp_max_pk)
        entry.a_b_mock = peak_to_ab(entry.b_mock, sp_max_pk)
        entry.a_c_mock = peak_to_ab(entry.c_mock, sp_max_pk)
        entry.a_a_wt = peak_to_ab(entry.a_wt, sp_max_pk)
        entry.a_b_wt = peak_to_ab(entry.b_wt, sp_max_pk)
        entry.a_c_wt = peak_to_ab(entry.c_wt, sp_max_pk)
        entry.a_a_delta_vif = peak_to_ab(entry.a_delta_vif, sp_max_pk)
        entry.a_b_delta_vif = peak_to_ab(entry.b_delta_vif, sp_max_pk)
        entry.a_c_delta_vif = peak_to_ab(entry.c_delta_vif, sp_max_pk)
        entry.save()
    except Exception as error_message:
        print(error_message)


# import routine to match original .csv file headers ("stored as verbose fields in django objects")
class Command(BaseCommand):
    """command to load regulatome data into django frm spreadsheets"""
    help = "command to load regulatome data"

    def add_arguments(self, parser):
        """type of measurement"""
        parser.add_argument('infile', type=str, help="input file")
        parser.add_argument('--type', type=str, help="data type,\
                             sp (Single Time Point) or tc (Time Course)")

    def handle(self, *args, **kwargs):
        """input reader"""
        os.getcwd()
        input_type = kwargs['type']
        all_fields = []
        if input_type == 'tc':
            all_fields = MultiTime._meta.get_fields()
        elif input_type == 'sp':
            all_fields = SingleTime._meta.get_fields()
        required_fields = [f for f in all_fields if not
                           (re.match(f.name, 'id') or
                            re.match("^(Abundance)", f.verbose_name) or
                            re.match(f.name, 'gene_id') or
                            re.match(f.name, 'uniq_gene_id'))]
        with open(os.path.join(os.getcwd(), kwargs['infile'])) as csvfile:
            reader = pd.read_csv(csvfile)
            for _, row in reader.iterrows():
                gene = populate_gene(row)
                if input_type == 'tc':
                    populate_multi_time(row, required_fields, gene)

                elif input_type == 'sp':
                    populate_single_time(row, required_fields, gene)
