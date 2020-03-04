import django_filters
from .models import Gene, SingleTime, MultiTime

class GeneFilter(django_filters.FilterSet):
    class Meta:
        model = Gene
        fields = {
                'gene_id': ['exact', ],
                'description': ['contains' ],
                'accession': ['exact'],
                'taxonomy': ['contains'],
                 }

class MultiTimeFilter(django_filters.FilterSet):
    #gene_id = django_filters.CharFilter(field_name='gene_id__gene_id', lookup_expr='icontains')
    class Meta:
        model = MultiTime 
        fields = {
                'gene_id__gene_id': ['exact','contains' ], 
                'log2_p48a_by_m48a': ['gt','lt'],
                'log2_n48a_by_m48a': ['gt', 'lt'],

                 }
        exclude = ['gene_id']

class SingleTimeFilter(django_filters.FilterSet):

    class Meta:
        model = SingleTime
        sequence = {'a_mock','b_mock','c_mock','a_wt', 'b_wt', 'c_wt','a_delta_vif', 'b_delta_vif', 'c_delta_vif'
                 }
        fields = {'a_mock': ['lt'],
                  'a_wt': ['gt'], 
                  'a_delta_vif' : ['gt'],
                  'gene_id__gene_id': ['exact', 'contains'],

                  }
        exclude = ['gene_id']

