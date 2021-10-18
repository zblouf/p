# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activity', '0002_prevactivityext_activity'),
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prevactivityext',
            name='equipments',
            field=models.ManyToManyField(related_name='equipments', to='equipment.Equipment'),
        ),
    ]
