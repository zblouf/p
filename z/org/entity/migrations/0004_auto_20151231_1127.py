# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 11:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0003_auto_20151231_0944'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together=set([('entity', 'name')]),
        ),
    ]
