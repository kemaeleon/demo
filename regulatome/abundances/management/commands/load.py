from django.core.management.base import BaseCommand, CommandError
from abundances.models import SingleTimePoint
import os, csv
print ("FOUND")
class Command(BaseCommand):
    def handle(self, *args, **options):
        (os.getcwd())
        with open(os.path.join(os.getcwd(),'data.csv')) as csvfile:
            reader = csv.DictReader(csvfile) 
            for row in reader:
                mv = 1.0
                print(row)
                headers = []
                for h in ('resting_1', 'resting_2',
                          'activated_1', 'activated_2',
                          'mock_24h', 'pos_24h', 'neg_24h',
                          'mock_48h', 'pos_48h', 'neg_48h'):
                    headers.append(float(row[h]))
                mv = max(headers)    
                print(mv) 
                e = SingleTimePoint(accession = row['accession'],
                                gene_id = row['gene_ID'],
                                description = row['description'],
                                taxonomy = row['taxonomy'],
                                protein_fdr_confidence_combined = row['protein_FDR_Confidence_Combined'],
                                missing_values = row['missing_Values'],
                                s_by_n = row['SBy_N'],
                                unique_peptides = row['unique_Peptides'],
                                r1_a = row['resting_1'],
                                r2_a = row['resting_2'],
                                a1_a = row['activated_1'],
                                a2_a = row['activated_2'],
                                m24_a = row['mock_24h'],
                                pos24_a = row['pos_24h'],
                                neg24_a = row['neg_24h'],
                                m48_a = row['mock_48h'],
                                pos48_a = row['pos_48h'],
                                neg48_a = row['neg_48h'],
                                r1 = round(float(row['resting_1'])/float(mv),2), 
                                r2 = round(float(row['resting_2'])/float(mv),2),
                                a1 = round(float( row['activated_1'])/float(mv),2), 
                                a2 = round(float(row['activated_2'])/float(mv),2), 
                                m24 = round(float(row['mock_24h'])/float(mv),2), 
                                pos24 = round(float(row['pos_24h'])/float(mv),2), 
                                neg24 = round(float(row['neg_24h'])/float(mv),2), 
                                m48 = round(float(row['mock_48h'])/float(mv),2),
                                pos48 = round(float(row['pos_48h'])/float(mv),2), 
                                neg48 = round(float(row['neg_48h'])/float(mv),2)) 
                               
                e.save()

