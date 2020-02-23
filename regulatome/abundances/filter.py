import django_filters
from .models import Gene, SingleTime, MultiTime

class GeneFilter(django_filters.FilterSet):
    class Meta:
        model = Gene
        fields = {
                'gene_id': ['exact', ],
                'description': ['contains' ],
                'accession': ['exact'],
                 }

class MultiTimeFilter(django_filters.FilterSet):
    class Meta:
        model = MultiTime
        fields = {
                'r1_a': ['exact', ],
                 }

class SingleTimeFilter(django_filters.FilterSet):
    class Meta:
        model = SingleTime
        fields = {
                'gene_id': ['exact', ],
                 }

