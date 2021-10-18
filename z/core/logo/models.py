from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.conf import settings
import os
from z.saas.models import Account

def upload_logo_to(inst, filename):
    return os.path.join(settings.ACCOUNT_DATA_ROOT, inst.account.login, 'logos')

@python_2_unicode_compatible
class Logo(models.Model):
    account = models.ForeignKey(Account, related_name='logo_owner')
    title = models.CharField(max_length=100, blank=True, default='')
    image = models.ImageField(  upload_to=upload_logo_to,
                                height_field='height',
                                width_field='width')
    height = models.PositiveIntegerField(blank=True, default=0)
    width = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return "[logo] %s" %(self.title)
