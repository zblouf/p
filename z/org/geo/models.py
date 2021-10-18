from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from z.saas.models import Account
from z.org.entity.models import Entity

@python_2_unicode_compatible
class Site(models.Model):
	account = models.ForeignKey(Account)
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True, default="")

// Todo : review Site/Zone affectation to Entities
@python_2_unicode_compatible
class EntitySite(models.Model):
	entity = models.ForeignKey(Entity)
	site = models.ForeignKey(Site)
	context = models.TexField(blank=True, default="")

@python_2_unicode_compatible
class Zone(models.Model):
	site = models.ForeignKey(Site)
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True, default="")
