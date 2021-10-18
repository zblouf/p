# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 09:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('saas', '0001_initial'),
        ('domain', '0003_auto_20151222_1750'),
        ('file', '0001_initial'),
        ('link', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hazard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shared', models.BooleanField(default=False)),
                ('creation_timestamp', models.DateTimeField(blank=True)),
                ('modification_timestamp', models.DateTimeField(blank=True)),
                ('deprecated', models.BooleanField(default=False)),
                ('cause', models.TextField()),
                ('consequence', models.TextField()),
                ('level', models.PositiveIntegerField(choices=[(1, 'minor injury'), (10, 'sick leave'), (100, 'permanent disability'), (1000, 'fatal')], default=1)),
                ('comment', models.TextField(blank=True, default='')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hazard_hazard_owned_by', to='saas.Account')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hazard_hazard_created_by', to=settings.AUTH_USER_MODEL)),
                ('docs', models.ManyToManyField(related_name='hazard_hazard_docs', to='file.DocFile')),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='domain.Domain')),
                ('links', models.ManyToManyField(related_name='hazard_hazard_links', to='link.DocLink')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hazard_hazard_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['domain', 'cause'],
            },
        ),
    ]
