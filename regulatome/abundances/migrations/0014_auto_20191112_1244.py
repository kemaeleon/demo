# Generated by Django 2.2.5 on 2019-11-12 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abundances', '0013_auto_20191112_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexabundance',
            name='single_time_tokens',
            field=models.CharField(default='', max_length=20, verbose_name='Snap'),
        ),
        migrations.AddField(
            model_name='indexabundance',
            name='time_course_tokens',
            field=models.CharField(default='', max_length=20, verbose_name='48h'),
        ),
    ]
