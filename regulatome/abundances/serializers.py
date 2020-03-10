from rest_framework import serializers
from .models import Gene, MultiTime, SingleTime


class GeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gene
        fields = ('gene_id', 'accession', 'description')


class MultiTimeSerializer(serializers.ModelSerializer):
    gene_id = GeneSerializer(many=False, read_only=True)

    class Meta:
        model = MultiTime
        fields = '__all__'


class SingleTimeSerializer(serializers.ModelSerializer):
    gene_id = GeneSerializer(many=False, read_only=True)

    class Meta:
        model = SingleTime
        fields = '__all__'
