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
    gene_id = django_filters.CharFilter(field_name='gene_id__gene_id', lookup_expr='icontains')
    gene_id = django_filters.CharFilter(field_name='gene_id__gene_id', lookup_expr='icontains')
    gene_id = django_filters.CharFilter(field_name='gene_id__gene_id', lookup_expr='icontains')
    class Meta:
        model = MultiTime
        fields = {
                'log2_p48a_by_m48a': ['gt'],
                'log2_n48a_by_m48a': ['lt'],
                 }
        exclude = ['gene_id']

class SingleTimeFilter(django_filters.FilterSet):
    class Meta:
        model = SingleTime
        fields = {
                'gene_id': ['exact', ],
                 }

