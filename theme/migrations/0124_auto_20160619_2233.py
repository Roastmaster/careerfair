# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 02:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0123_auto_20160618_0347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='sponsor',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]