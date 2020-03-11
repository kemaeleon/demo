import attributedict
from django.utils.safestring import mark_safe
import django_tables2 as tables
from django_tables2.utils import A, Accessor, AttributeDict
from .models import Gene, MultiTime, SingleTime


class NumberColumn(tables.Column):
    def render(self, value):
        return '{:0.2f}'.format(value)


class SmallValColumn(tables.Column):
    def render(self, value):
        return '{:0.2E}'.format(value)


class myColumn(tables.CheckBoxColumn):

    @property
    def header(self):
        default = {"type": "checkbox", "onkeyup": "success"}
        general = self.attrs.get("input")
        specific = self.attrs.get("th__input")
        attrs = AttributeDict(default, **(specific or general or {}))
        return mark_safe("<input %s/>" % attrs.as_html())

    def render(self, value, bound_column, record):
        default = {"type": "checkbox",\
                "name": bound_column.name, "value": value, "onclick": "success()", }
        if self.is_checked(value, record):
            default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = AttributeDict(default, **(specific or general or {}))
        return mark_safe("<input %s/>" % attrs.as_html())


class MultiTimeTable(tables.Table):
    ttype = 'MT'
    # selected = tables.CheckBoxColumn(accessor='pk', orderable=False)
    selected = myColumn(accessor='pk', orderable=False)

    class Meta:
        model = MultiTime
        sequence = ('selected', 'gene_id.gene_id')
        fields = (
            'gene_id.gene_id', 'gene_id.accession',\
            'gene_id.description', 'log2_p24a_by_m24a', 'log2_n24a_by_m24a',\
            'log2_p48a_by_m48a', 'log2_n48a_by_m48a')
        attrs = {"class": "table table-striped table-hover table-responsive w-auto"}

    def render_edit(self):
        return 'Edit'


class SingleTimeTable(tables.Table):
    ttype = 'st'
    tid = ''
    selected = myColumn(accessor='pk', orderable=False)
    log2_wt_by_mock = NumberColumn()
    q_wt_by_mock = SmallValColumn(
        attrs={'td': {'class': lambda value: 'bg-primary' if float(value) < 0.05 else 'bg-light'}})
    p_wt_by_mock = SmallValColumn(
        attrs={'td': {'class': lambda value: 'bg-primary' if float(value) < 0.05 else 'bg-light'}})

    class Meta:
        model = SingleTime
        sequence = ('selected', 'gene_id.gene_id')
        fields = ('gene_id.gene_id', 'log2_wt_by_mock', 'q_wt_by_mock',\
                  'p_wt_by_mock', 'a_a_wt', 'a_b_wt', 'a_c_wt',
                  'a_a_delta_vif', 'a_b_delta_vif', 'a_c_delta_vif')
        attrs = {"class": "table table-striped table-hover table-responsive w-auto"}

    def render_edit(self):
        return 'Edit'


class GeneTable(tables.Table):
    selected = myColumn(accessor='pk', orderable=False)

    class Meta:
        model = Gene
        sequence = ('selected', 'gene_id', 'accession', 'description', 'taxonomy')
        fields = ('gene_id', 'accession', 'description', 'taxonomy')
        attrs = {"class": "table table-striped table-hover table-responsive w-auto"}

    def render_edit(self):
        return 'Edit'


class StatsTable(tables.Table):
    Ab = tables.Column()
    log2 = NumberColumn()
    pValue = SmallValColumn(attrs={'td':\
            {'class': lambda value: 'bg-primary' if float(value) < 0.05 else 'bg-light'}})
    qValue = SmallValColumn(attrs={'td':\
            {'class': lambda value: 'bg-primary' if float(value) < 0.05 else 'bg-light'}})
