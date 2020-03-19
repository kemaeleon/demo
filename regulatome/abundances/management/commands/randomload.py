"""module to generate random data to test data retrieval speeds"""
import random
import string
import itertools
from django.core.management.base import BaseCommand
from abundances.models import SingleTime

def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    """random entry for accession field"""
    # return str(''.join(random.choice(chars) for x_value in range(size)))
    return str(''.join(random.choice(chars) for _ in itertools.repeat(None, size)))

def random_number():
    """random number for raw abundances"""
    return random.random()*100

def random_fraction():
    """random number for fractions"""
    return random.random()


class Command(BaseCommand):
    """procedure to populate database with random SingleTime entries"""
    def handle(self, *args, **options):
        for _ in itertools.repeat(None, 10):
            entry = SingleTime(accession=random.randint(1, 100),\
                gene_id=random_string(),\
                description="random zebra",\
                taxonomy="zebra",\
                protein_fdr_confidence_combined="high",\
                missing_values=0,\
                s_by_n=1,\
                unique_peptides=1,\
                r1_a=random_number(),\
                r2_a=random_number(),\
                a1_a=random_number(),\
                a2_a=random_number(),\
                m24_a=random_number(),\
                pos24_a=random_number(),\
                neg24_a=random_number(),\
                m48_a=random_number(),\
                pos48_a=random_number(),\
                neg48_a=random_number(),\
                r1=random_fraction(),\
                r2=random_fraction(),\
                a1=random_fraction(),\
                a2=random_fraction(),\
                m24=random_fraction(),\
                pos24=random_fraction(),\
                neg24=random_fraction(),\
                m48=random_fraction(),\
                pos48=random_fraction(),\
                neg48=random_fraction())
            entry.save()
