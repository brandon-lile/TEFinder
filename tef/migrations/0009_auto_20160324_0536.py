# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-24 05:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tef', '0008_te_reverse_query'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='te',
            name='end_loc',
        ),
        migrations.RemoveField(
            model_name='te',
            name='start_loc',
        ),
    ]