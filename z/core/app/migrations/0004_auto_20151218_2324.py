# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20151218_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appregistration',
            name='account',
            field=models.ForeignKey(to='saas.Account', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appregistration',
            name='app',
            field=models.ForeignKey(to='app.App', blank=True, null=True),
        ),
    ]
