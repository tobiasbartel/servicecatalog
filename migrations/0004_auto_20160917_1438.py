# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicecatalog', '0003_auto_20160917_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
