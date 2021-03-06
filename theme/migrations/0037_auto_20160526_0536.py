# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-26 09:36
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0036_auto_20160526_0435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='website',
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='website',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='resume',
            field=mezzanine.core.fields.FileField(blank=True, max_length=255),
        ),
    ]
