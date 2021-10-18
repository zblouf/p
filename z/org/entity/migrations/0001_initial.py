# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('account', models.ForeignKey(to='saas.Account')),
            ],
        ),
        migrations.CreateModel(
            name='EntitySpec',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('entity', models.ForeignKey(to='entity.Entity')),
            ],
        ),
    ]
