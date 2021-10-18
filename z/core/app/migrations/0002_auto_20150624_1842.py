# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0001_initial'),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appregistration',
            name='account',
            field=models.ForeignKey(to='saas.Account'),
        ),
        migrations.AddField(
            model_name='appregistration',
            name='app',
            field=models.ForeignKey(to='app.App'),
        ),
        migrations.AlterUniqueTogether(
            name='appregistration',
            unique_together=set([('app', 'account')]),
        ),
    ]
