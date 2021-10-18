# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=100, help_text='account complete name')),
                ('login', models.SlugField(verbose_name='login', help_text='account identifier, composed of alphanumeric characters', unique=True)),
                ('maintenance_message', models.TextField(verbose_name='maintenance message', blank=True, default='')),
                ('logo', models.ForeignKey(related_name='account_primary_logo', null=True, blank=True, to='logo.Logo')),
            ],
            options={
                'verbose_name': 'account',
                'ordering': ('login', 'name'),
            },
        ),
    ]
