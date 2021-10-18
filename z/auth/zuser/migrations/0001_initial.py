# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ZUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.PositiveIntegerField(default=0, choices=[(0, 'Standard'), (10, 'Retail'), (42, 'Superadmin')])),
                ('is_admin', models.BooleanField(default=False)),
                ('is_generic', models.BooleanField(default=False)),
                ('generic_prefix', models.CharField(max_length=100, blank=True, default='')),
                ('phone', models.CharField(verbose_name='phone number', max_length=100, blank=True, default='')),
                ('position', models.CharField(verbose_name='position/post', max_length=100, blank=True, default='')),
                ('comment', models.TextField(verbose_name='comment', blank=True, default='')),
                ('account', models.ForeignKey(to='saas.Account', default=None, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__username'],
            },
        ),
    ]
