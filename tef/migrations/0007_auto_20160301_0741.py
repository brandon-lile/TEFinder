# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tef', '0006_auto_20160301_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='te',
            name='end_loc',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='te',
            name='start_loc',
            field=models.IntegerField(default=0),
        ),
    ]
