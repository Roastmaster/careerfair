# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-24 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0129_auto_20160724_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationpage',
            name='email_template_html',
        ),
        migrations.RemoveField(
            model_name='registrationpage',
            name='email_template_text',
        ),
        migrations.AddField(
            model_name='registrationpage',
            name='invoice_template_html',
            field=models.FileField(blank=True, help_text='Should be identical to the text template except with added html', upload_to='uploads/company_iamges', verbose_name='Invoice HTML Template'),
        ),
        migrations.AddField(
            model_name='registrationpage',
            name='invoice_template_text',
            field=models.FileField(blank=True, help_text='Text template of invoice in case html version does not render', upload_to='uploads/company_images', verbose_name='Invoice Text Template'),
        ),
    ]
