from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from z.saas.models import Account

@python_2_unicode_compatible
class App(models.Model):
    name = models.CharField(max_length=100)
    namespace = models.SlugField()
    decription = models.TextField(blank=True, default='')

    def __str__(self):
        return "%s (%s)" %(self.name, self.namespace)

class AppRegistration(models.Model):
    app = models.ForeignKey(App, null=True, blank=True)
    account = models.ForeignKey(Account, null=True, blank=True)
    value = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('app', 'account')

    def __str__(self):
        return "%s - %s" %(self.account, self.app)

