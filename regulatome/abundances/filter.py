import django_filters
from .models import Gene

class GeneFilter(django_filters.FilterSet):
    class Meta:
        model = Gene
        fields = {
                'gene_id': ['exact', ],
                'description': ['exact','contains' ],
                'accession': ['exact','contains' ],
                'taxonomy': ['exact','contains'],
                 }



