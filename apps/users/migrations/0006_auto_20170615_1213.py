# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-15 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_emailverifyrecord_is_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '\u6ce8\u518c'), ('forget', '\u627e\u56de\u5bc6\u7801'), ('update_email', '\u66f4\u6539\u90ae\u7bb1')], max_length=30, verbose_name='\u53d1\u9001\u7c7b\u578b'),
        ),
    ]
