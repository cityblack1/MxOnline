# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-31 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='notice',
            field=models.CharField(default='', max_length=100, verbose_name='\u8bfe\u7a0b\u516c\u544a'),
        ),
    ]
