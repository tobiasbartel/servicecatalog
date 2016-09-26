# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicecatalog', '0013_auto_20160917_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmethod',
            name='method',
            field=models.CharField(choices=[('lync', 'Lync'), ('email', 'EMail'), ('phone', 'Office Phone'), ('mobile', 'Mobile Phone'), ('web', 'Web'), ('ocd', 'On Call'), ('ticket', 'Ticketing (Web)')], max_length=10),
        ),
    ]