import django_filters
from .models import TimeCourse, IndexAbundance, SingleTimePoint,Gene

class GeneFilter(django_filters.FilterSet):
    class Meta:
        model = Gene
        fields = {
                'gene_id': ['exact', ],
                'description': ['exact','contains' ],
                'accession': ['exact','contains' ],
                'taxonomy': ['exact','contains'],
                 }


class TimeCourseFilter(django_filters.FilterSet):
    class Meta:
        model = TimeCourse
        fields = {
                'gene_id': ['exact', ],
                'description': ['exact','contains' ],
                'log2_p48a_by_m48a': ['lt'],
                'log2_n48a_by_m48a': ['gt'],
                 }


class SingleTimePointFilter(django_filters.FilterSet):
    class Meta:
        model = SingleTimePoint
        fields = {
                'gene_id': ['exact', ],
                'description': ['exact','contains' ],
                 }


class IndexFilter(django_filters.FilterSet):
    class Meta:
        model = IndexAbundance
        fields = {
                'gene_id': ['exact', ],
                 }

