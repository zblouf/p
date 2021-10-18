from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from z.meta.option.models import Option
import os
#import reversion
from django.conf import settings

ACCOUNT_MEDIA_PATHLIST = (
    '',
    'logos',
    'docs',    
)

@python_2_unicode_compatible
#@reversion.register
class Account(models.Model):
	name = models.CharField(max_length=100, verbose_name=_("name"),
							help_text=_('account complete name'))
	login = models.SlugField(unique=True, verbose_name=_("login"),
							help_text=_('account identifier, composed of alphanumeric characters'))
	maintenance_message = models.TextField(blank=True, default="", 
							verbose_name=_('maintenance message'))
	logo = models.ForeignKey("logo.Logo", blank=True, null=True, related_name="account_primary_logo")

	options = GenericRelation(Option)

	class Meta:
		verbose_name = _("account")
		ordering = ('login', 'name')

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		for path in ACCOUNT_MEDIA_PATHLIST:
			_path = os.path.join(settings.ACCOUNT_DATA_ROOT, self.login, path)
			if not os.path.exists(_path):
				os.mkdir(_path)
		super(Account, self).save(*args, **kwargs)

	@property
	def logo_url(self):
		filename = self.logo.image.name
		if filename[:1]=="/":
			filename = filename[len(settings.ACCOUNT_DATA_ROOT)+1:]
		return settings.MEDIA_URL+filename
