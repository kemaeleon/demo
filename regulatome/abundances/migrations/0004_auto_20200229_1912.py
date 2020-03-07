# Generated by Django 2.2.4 on 2020-02-29 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abundances', '0003_auto_20200221_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='singletime',
            name='a_a_delta_vif',
            field=models.FloatField(default=0.0, verbose_name='A_ΔVif'),
        ),
        migrations.AddField(
            model_name='singletime',
            name='a_a_mock',
            field=models.FloatField(default=0.0, verbose_name='A_Mock'),
        ),
        migrations.AddField(
            model_name='singletime',
            name='a_a_wt',
            field=models.FloatField(default=0.0, verbose_name='A_WT'),
        ),
        migrations.AddField(
            model_name='singletime',
            name='a_b_delta_vif',
            field=models.FloatField(default=0.0, verbose_name='B_ΔVif'),
        ),
        migrations.AddField(
            model_name='singletime',
            name='a_b_mock',
            field=models.FloatField(default=0.0, verbose_name='B_Mock'),
        ),
        migrations.AddField(
            model_name='singletime',
            name='a_b_wt',
            field=models.FloatField(default=0.0, verbose_name='B_WT'),
        ),
        migrations.AddField(
            model_name='singletime',
            name='a_c_delta_vif',
            field=models.FloatField(default=0.0, verbose_name='C_ΔVif'),
        ),
        migrations.AddField(
            model_name='singletime',
            name='a_c_mock',
            field=models.FloatField(default=0.0, verbose_name='C_Mock'),
        ),
        migrations.AddField(
            model_name='singletime',
            name='a_c_wt',
            field=models.FloatField(default=0.0, verbose_name='C_WT'),
        ),
    ]