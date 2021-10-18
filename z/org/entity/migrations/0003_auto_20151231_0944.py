# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
        ('entity', '0002_auto_20151231_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='equipments',
            field=models.ManyToManyField(related_name='activity_equipments', to='equipment.Equipment'),
        ),
        migrations.AddField(
            model_name='activity',
            name='info',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
        migrations.AddField(
            model_name='unit',
            name='info',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
    ]