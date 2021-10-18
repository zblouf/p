# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0001_initial'),
        ('logo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logo',
            name='account',
            field=models.ForeignKey(related_name='logo_owner', to='saas.Account'),
        ),
    ]
