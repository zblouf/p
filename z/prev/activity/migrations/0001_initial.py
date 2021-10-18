# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 09:35
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PrevActivityExt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prev_comment', models.TextField(blank=True, default='')),
                ('info', jsonfield.fields.JSONField(blank=True, default={})),
            ],
        ),
    ]
