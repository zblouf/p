from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from z.meta.abstract.models import DocModel, TrackedOwnedModel
from z.saas.models import Account

@python_2_unicode_compatible
class SectorAccountManager(models.Manager):
    def for_account(self, account=""):
        a = None
        if isinstance(account, Account):
            a = account
        elif isinstance(account, str) or isinstance(account, unicode):
            alist = Account.objects.filter(login=account)
            if len(alist)>0:
                a = alist[0]
        else:
            raise Exception("Argument is not a valid account instance or reference")
#        _owned_sectors = super(SectorCustomerManager, self).get_queryset().filter(custowner=c)
#        _registered_sectors = super(SectorCustomerManager, self).get_queryset().filter(sectorregistration__customer=c)
        _owned_sectors = self.filter(account=a)
        _registered_sectors = self.filter(sectorregistration__account=a)
        return _owned_sectors | _registered_sectors

@python_2_unicode_compatible
class Sector(DocModel, TrackedOwnedModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    comment = models.TextField(blank=True, default="")
    objects = SectorAccountManager()

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class DomainAccountManager(models.Manager):
    def for_account(self, account=""):
        a = None
        if isinstance(account, Account):
            a = account
        elif isinstance(account, str) or isinstance(account, unicode):
            alist = Account.objects.filter(login=Account)
            if len(alist)>0:
                a = alist[0]
        else:
            raise Exception("Argument is not a valid account instance or reference")
        _owned_domains = super(DomainAccountManager, self).get_queryset().filter(account=a)
        _registered_domains = super(DomainAccountManager, self).get_queryset().filter(domainregistration__account=a)
        _herited_domains = super(DomainAccountManager, self).get_queryset().filter(sector__sectorregistration__account=a, sector__sectorregistration__recursive=True)
        print ("owned : %s" %(repr(_owned_domains)))
        print ("registered : %s" %(repr(_registered_domains)))
        print ("herited : %s" %(repr(_herited_domains)))
        return _owned_domains | _registered_domains | _herited_domains

@python_2_unicode_compatible
class Domain(DocModel, TrackedOwnedModel):
    sector = models.ForeignKey(Sector)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    comment = models.TextField(blank=True, default="")    

    objects = DomainAccountManager()

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class SectorRegistration(models.Model):
    account = models.ForeignKey(Account)
    sector = models.ForeignKey(Sector)
    recursive = models.BooleanField(default=True)

@python_2_unicode_compatible
class DomainRegistration(models.Model):
    account = models.ForeignKey(Account)
    domain = models.ForeignKey(Domain)
