# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-24 06:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tef', '0011_auto_20160324_0555'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solution',
            old_name='search',
            new_name='te',
        ),
    ]