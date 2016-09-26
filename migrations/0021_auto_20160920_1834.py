# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 18:34
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('servicecatalog', '0020_auto_20160920_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='hardware_depending_on_hardware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port_numbers', models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('depending_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hardware_target', to='servicecatalog.Hardware')),
                ('hardware', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hardware_source', to='servicecatalog.Hardware')),
            ],
        ),
        migrations.CreateModel(
            name='hardware_depending_on_instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port_numbers', models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('hardware', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hardware_depending', to='servicecatalog.Hardware')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instance_depended_on', to='servicecatalog.Instance')),
            ],
        ),
        migrations.AddField(
            model_name='hardware',
            name='depending_on_hardware',
            field=models.ManyToManyField(blank=True, default=None, through='servicecatalog.hardware_depending_on_hardware', to='servicecatalog.Hardware'),
        ),
        migrations.AddField(
            model_name='hardware',
            name='depending_on_instance',
            field=models.ManyToManyField(blank=True, null=True, through='servicecatalog.hardware_depending_on_instance', to='servicecatalog.Instance'),
        ),
    ]
