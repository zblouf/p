from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.auth.models import User
from z.saas.models import Account

@python_2_unicode_compatible
class Vendor(models.Model):
	name = models.CharField(max_length=100, verbose_name=_("name"),
							help_text=_("complete name for vendor"))
	login = models.SlugField(blank=True, default="")

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Agent(models.Model):
	user = models.ForeignKey(User)
	vendor = models.ForeignKey(Vendor)

	def __str__(self):
		return "%s (%s)" %(self.user, self.vendor)

@python_2_unicode_compatible
class VendorAccount(models.Model):
	vendor = models.ForeignKey(Vendor)
	agent = models.ForeignKey(Agent)
	account = models.ForeignKey(Account)
