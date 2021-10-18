# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import z.core.logo.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True, default='')),
                ('image', models.ImageField(upload_to=z.core.logo.models.upload_logo_to, height_field='height', width_field='width')),
                ('height', models.PositiveIntegerField(blank=True, default=0)),
                ('width', models.PositiveIntegerField(blank=True, default=0)),
            ],
        ),
    ]
