import django_tables2 as tables
from django_tables2.utils import A 
from .models import TimeCourse, IndexAbundance, SingleTimePoint,Gene,MultiTime,SingleTime


class MultiTimeTable(tables.Table):
    ttype = 'MT'
    gene_id = tables.Column(linkify = True)
    selected = tables.CheckBoxColumn(accessor='pk', orderable=False)
    class Meta:
        model = MultiTime
        sequence = ('selected','gene_id')
        fields = ('gene_id','gene_id.gene_id','gene_id.accession', 'gene_id.description','log2_p24a_by_m24a','log2_n24a_by_m24a','log2_p48a_by_m48a','log2_n48a_by_m48a')
        attrs = {"class": "table table-striped table-hover table-responsive w-auto"}
    def render_edit(self):
        return 'Edit'

class SingleTimeTable(tables.Table):
    ttype = 'st'
    gene_id = tables.Column(linkify = True)
    selected = tables.CheckBoxColumn(accessor='pk', orderable=False)
    class Meta:
        model = SingleTimePoint
        sequence = ('selected','gene_id')
        fields = ('gene_id','a_mock','b_mock','c_mock','a_wt', 'b_wt', 'c_wt','a_delta_vif', 'b_delta_vif', 'c_delta_vif')
        attrs = {"class": "table table-striped table-hover table-responsive w-auto"}
    def render_edit(self):
        return 'Edit'




class PeakTable(tables.Table):
    ttype = 'tc'
    gene_id = tables.Column(linkify = True)
    selected = tables.CheckBoxColumn(accessor='pk', orderable=False)
    class Meta:
        model = TimeCourse
        sequence = ('selected','gene_id')
        fields = ('gene_id','accession', 'description','log2_p24a_by_m24a','log2_n24a_by_m24a','log2_p48a_by_m48a','log2_n48a_by_m48a') 
        attrs = {"class": "table table-striped table-hover table-responsive w-auto"}
    def render_edit(self):
        return 'Edit'    


class SingleTimePointTable(tables.Table):
    ttype = 'st'
    gene_id = tables.Column(linkify = True)
    selected = tables.CheckBoxColumn(accessor='pk', orderable=False)
    class Meta:
        model = SingleTimePoint
        sequence = ('selected','gene_id')
        fields = ('gene_id','a_mock','b_mock','c_mock','a_wt', 'b_wt', 'c_wt','a_delta_vif', 'b_delta_vif', 'c_delta_vif') 
        attrs = {"class": "table table-striped table-hover table-responsive w-auto"}
    def render_edit(self):
        return 'Edit'    


class GeneTable(tables.Table):
    selected = tables.CheckBoxColumn(accessor='pk', orderable=False)
    class Meta:
        model = Gene
        sequence = ('selected','gene_id','accession','description','taxonomy')
        fields = ('gene_id','accession','description','taxonomy')
        attrs = {"class": "table table-striped table-hover table-responsive w-auto"}
    def render_edit(self):
        return 'Edit'


class IndexTable(tables.Table):
    gene_id = tables.Column()
    selected = tables.CheckBoxColumn(accessor='pk', orderable=False)
    class Meta:
        model = IndexAbundance
        sequence = ('selected','gene_id')
        fields = ('gene_id','time_course_tokens','single_time_tokens') 
        attrs = {"class": "table table-striped table-hover table-responsive w-auto"}
    def render_edit(self):
        return 'Edit'    

