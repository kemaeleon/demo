"""module defining the database fields available via the admin interface"""
from django.contrib import admin
from .models import Gene, MultiTime, SingleTime


class GeneAdmin(admin.ModelAdmin):
    """general protein info fields in admin interface"""
    search_fields = ('id', 'gene_id', 'description', 'accession', 'taxonomy')
    list_display = ('id', 'gene_id', 'description', 'accession', 'taxonomy')
    list_per_page = 30
    save_on_top = True

class SingleTimeAdmin(admin.ModelAdmin):
    """single time fields in admin interface"""
    search_fields = ('gene_id', 'description')
    list_display = ('gene_id', 'a_a_wt')



class MultiTimeAdmin(admin.ModelAdmin):
    """multi time fields in admin interface"""
    search_fields = ('gene_id', 'description')
    list_display = ('gene_id', 'log2_p48a_by_m48a', 'log2_n48a_by_m48a')


admin.site.register(Gene, GeneAdmin)
admin.site.register(MultiTime, MultiTimeAdmin)
admin.site.register(SingleTime, SingleTimeAdmin)
