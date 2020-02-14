from django.contrib import admin
from .models import TimeCourse


class PeakAdmin(admin.ModelAdmin):
    search_fields = ('gene_id', 'description','pos24')
    #fields = ('gene_id', 'description' ,'pos24')
    list_display = ('gene_id', 'description','pos24')
    list_per_page = 15
    save_on_top = True


admin.site.register(TimeCourse,PeakAdmin)
