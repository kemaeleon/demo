"""models module"""
from django.db import models

class Gene(models.Model):
    """taxonomic information about the protein"""
    gene_id = models.CharField("Gene ID", max_length=15, default="")
    accession = models.CharField("Accession", max_length=10, default="")
    description = models.CharField("Description", max_length=80, default="")
    taxonomy = models.CharField("Taxonomy", max_length=20, default="")
    class Meta:
        constraints = [
            models.UniqueConstraint(\
            fields=['gene_id', 'accession', 'description', 'taxonomy'],\
            name='unique_entry'),]

class SingleMultiAbundance(models.Model):
    """base model for regulatome measurements"""
    class Meta:
        abstract = True

    uniq_gene_id = models.CharField("uniq_gene_id", max_length=200, default="")
    protein_fdr_confidence_combined =\
            models.CharField("Protein FDR Confidence: Combined", max_length=10, default="")
    missing_values = models.FloatField("Missing values", default=0)
    s_by_n = models.FloatField("Log10(S/N)", default=999)


class SingleTime(SingleMultiAbundance):
    """single time point measurements"""
    greek_d = "\N{GREEK CAPITAL LETTER DELTA}"
    gene_id = models.ForeignKey(Gene, on_delete=models.CASCADE)
    log2_wt_by_mock = models.FloatField("Log2(WT/Mock)", default=1.0)
    p_wt_by_mock = models.FloatField("p_WT/Mock", default=1.0)
    q_wt_by_mock = models.FloatField("q_WT/Mock", default=1.0)
    log2_delta_vif_by_mock = models.FloatField("Log2(" + greek_d + "Vif/Mock)", default=1.0)
    p_delta_vif_by_mock = models.FloatField("p_" + greek_d + "Vif/Mock", default=1.0)
    q_delta_vif_by_mock = models.FloatField("q_" + greek_d + "Vif/Mock", default=1.0)
    log2_wt_by_delta_vif = models.FloatField("Log2(WT/" + greek_d + "Vif)", default=1.0)
    p_wt_by_delta_vif = models.FloatField("p_WT/" + greek_d + "Vif", default=1.0)
    q_wt_by_delta_vif = models.FloatField("q_WT/" + greek_d + "Vif", default=1.0)
    a_mock = models.FloatField("A_Mock", default=1.0)
    b_mock = models.FloatField("B_Mock", default=1.0)
    c_mock = models.FloatField("C_Mock", default=1.0)
    a_wt = models.FloatField("A_WT", default=1.0)
    b_wt = models.FloatField("B_WT", default=1.0)
    c_wt = models.FloatField("C_WT", default=1.0)
    a_delta_vif = models.FloatField("A_" + greek_d + "Vif", default=1.0)
    b_delta_vif = models.FloatField("B_" + greek_d + "Vif", default=1.0)
    c_delta_vif = models.FloatField("C_" + greek_d + "Vif", default=1.0)
    a_a_mock = models.FloatField("A_Mock", default=0.0)
    a_b_mock = models.FloatField("B_Mock", default=0.0)
    a_c_mock = models.FloatField("C_Mock", default=0.0)
    a_a_wt = models.FloatField("A_WT", default=0.0)
    a_b_wt = models.FloatField("B_WT", default=0.0)
    a_c_wt = models.FloatField("C_WT", default=0.0)
    a_a_delta_vif = models.FloatField("A_" + greek_d + "Vif", default=0.0)
    a_b_delta_vif = models.FloatField("B_" + greek_d + "Vif", default=0.0)
    a_c_delta_vif = models.FloatField("C_" + greek_d + "Vif", default=0.0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['gene_id',
                        'log2_wt_by_mock', 'p_wt_by_mock', 'q_wt_by_mock', 'log2_delta_vif_by_mock',
                        'p_wt_by_delta_vif', 'q_wt_by_delta_vif',
                        'a_mock', 'b_mock', 'c_mock',
                        'a_wt', 'b_wt', 'c_wt',
                        'a_delta_vif', 'b_delta_vif', 'c_delta_vif'], name='unique_entry'),
                        ]

    def get_absolute_url(self):
        """return url for linking e.g. a table column to the data entry"""
        return "/rest/uniq-gene-id-%s" % self.uniq_gene_id


class MultiTime(SingleMultiAbundance):
    """class for multi time point measurements"""
    greek_d = "\N{GREEK CAPITAL LETTER DELTA}"
    gene_id = models.ForeignKey(Gene, on_delete=models.CASCADE)
    r1_a = models.FloatField("Abundance Resting_1", default=1.0)
    r2_a = models.FloatField("Abundance Resting_2", default=1.0)
    a1_a = models.FloatField("Abundance Activated_1", default=1.0)
    a2_a = models.FloatField("Abundance Activated_2", default=1.0)
    m24_a = models.FloatField("Abundance 24h_Mock", default=1.0)
    pos24_a = models.FloatField("Abundance 24h_Pos", default=1.0)
    neg24_a = models.FloatField("Abundance 24h_Neg", default=1.0)
    m48_a = models.FloatField("Abundance 48h_Mock", default=1.0)
    pos48_a = models.FloatField("Abundance 48h_Pos", default=1.0)
    neg48_a = models.FloatField("Abundance 48h_Neg", default=1.0)
    log2_r1a_by_r2a = models.FloatField("Abundance Resting Lg2Ratio", default=1.0)
    log2_a1a_by_a2a = models.FloatField("Abundance Activated Lg2Ratio", default=1.0)
    log2_p24a_by_m24a = models.FloatField("Abundance Positive 24 Lg2Ratio", default=1.0)
    log2_n24a_by_m24a = models.FloatField("Abundance Negative 24 Lg2Ratio", default=1.0)
    log2_p48a_by_m48a = models.FloatField("Abundance Positive 48 Lg2Ratio", default=1.0)
    log2_n48a_by_m48a = models.FloatField("Abundance Negative 48 Lg2Ratio", default=1.0)
    r1 = models.FloatField("Resting_1", default=1.0)
    r2 = models.FloatField("Resting_2", default=1.0)
    a1 = models.FloatField("Activated_1", default=1.0)
    a2 = models.FloatField("Activated_2", default=1.0)
    m24 = models.FloatField("24h_Mock", default=1.0)
    pos24 = models.FloatField("24h_Pos", default=1.0)
    neg24 = models.FloatField("24h_Neg", default=1.0)
    m48 = models.FloatField("48h_Mock", default=1.0)
    pos48 = models.FloatField("48h_Pos", default=1.0)
    neg48 = models.FloatField("48h_Neg", default=1.0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['gene_id',
                                            'r1', 'r2', 'a1', 'a2',
                                            'm24', 'pos24', 'neg24',
                                            'm48', 'pos48', 'neg48'],\
                                            name='unique_entry'),]

    def get_absolute_url(self):
        """return url for linking e.g. a table column to the data entry"""
        return "/rest/multi-time-id-%s" % self.id
