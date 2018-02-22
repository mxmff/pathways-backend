# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-21 00:46
from __future__ import unicode_literals

import common.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20171214_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceAtLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Location')),
            ],
            bases=(common.models.ValidateOnSaveMixin, models.Model),
        ),
    ]