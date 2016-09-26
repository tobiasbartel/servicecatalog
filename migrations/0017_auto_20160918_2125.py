# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicecatalog', '0016_auto_20160918_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='state',
            field=models.CharField(choices=[('dev', 'In development'), ('live', 'Live'), ('depricated', 'Depricated')], default='live', max_length=10),
        ),
    ]
