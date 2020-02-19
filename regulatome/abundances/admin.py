from django.contrib import admin
from .models import Gene,MultiTime


class GeneAdmin(admin.ModelAdmin):
    search_fields = ('id', 'gene_id', 'description', 'accession','taxonomy')
    list_display = ('id', 'gene_id', 'description','accession','taxonomy')
    list_per_page = 30
    save_on_top = True

class MultiTimeAdmin(admin.ModelAdmin):
    search_fields = ('gene_id', 'description')
    list_display = ('gene_id', 'log2_p48a_by_m48a', 'log2_n48a_by_m48a')


admin.site.register(Gene,GeneAdmin)
admin.site.register(MultiTime,MultiTimeAdmin)
