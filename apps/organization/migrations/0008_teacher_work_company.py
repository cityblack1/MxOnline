# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-01 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_auto_20170510_0245'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='work_company',
            field=models.CharField(default='\u5927\u82f1\u5e1d\u56fd', max_length=50, verbose_name='\u5de5\u4f5c\u516c\u53f8'),
        ),
    ]
