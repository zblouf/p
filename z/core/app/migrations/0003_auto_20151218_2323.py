# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150624_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appregistration',
            name='account',
            field=models.ForeignKey(to='saas.Account', null=True),
        ),
        migrations.AlterField(
            model_name='appregistration',
            name='app',
            field=models.ForeignKey(to='app.App', null=True),
        ),
    ]
