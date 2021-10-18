from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from z.org.entity.models import Entity

@python_2_unicode_compatible
class Position(models.Model):
    name = models.CharField(max_length=200, default="")
    description = models.TextField(blank=True, default="")
    entity = models.ForeignKey(Entity, blank=True, null=True, default=None)

@python_2_unicode_compatible
class Employee(models.Model):
    firstname = models.CharField(max_length=100, blank=True, default="")
    lastname = models.CharField(max_length=100, blank=True, default="")
