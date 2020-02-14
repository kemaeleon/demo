from django.core.management.base import BaseCommand, CommandError
from abundances.models import SingleTimePoint
import os, csv
import random, string
print ("FOUND")
def rs(size=6, chars=string.ascii_uppercase + string.digits):
    return str(''.join(random.choice(chars) for x in range(size)))

def rf():
    return random.random()*100

def rf2():
    return random.random()


class Command(BaseCommand):
    def handle(self, *args, **options):
        for x in range(10):
            e = SingleTimePoint(accession = random.randint(1,100) ,
                gene_id = rs(),
                description = "random zebra",
                taxonomy = "zebra",
                protein_fdr_confidence_combined = "high",
                missing_values = 0,
                s_by_n = 1,
                unique_peptides = 1,
                r1_a = rf(),
                r2_a = rf(),
                a1_a = rf(),
                a2_a = rf(),
                m24_a = rf(),
                pos24_a = rf(),
                neg24_a = rf(),
                m48_a = rf(),
                pos48_a = rf(),
                neg48_a = rf(),
                r1 = rf2(), 
                r2 = rf2(),
                a1 = rf2(), 
                a2 = rf2(),
                m24 = rf2(),
                pos24 = rf2(),
                neg24 = rf2(),
                m48 = rf2(),
                pos48 = rf2(),
                neg48 = rf2())
            e.save()

