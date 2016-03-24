# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-24 05:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tef', '0010_te_distance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.TextField(null=True)),
                ('percentage', models.DecimalField(decimal_places=1, max_digits=3)),
                ('distance', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='te',
            name='solution',
        ),
        migrations.AddField(
            model_name='solution',
            name='search',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tef.TE'),
        ),
    ]
