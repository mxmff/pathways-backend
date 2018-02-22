# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-31 23:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0007_auto_20180126_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationaddress',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='addresses.Address'),
        ),
    ]