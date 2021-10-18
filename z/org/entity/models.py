from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from z.meta.abstract.models import InfoDictModel
from z.means.equipment.models import Equipment

from django.db import models
from z.saas.models import Account

@python_2_unicode_compatible
class Entity(InfoDictModel):
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=200)
    ref = models.ForeignKey('self', null=True, blank=True, related_name='refs')
    ref_active = models.BooleanField(default=False)

    coordinates = JSONField(blank=True, default={})

    def __str__(self):
        return self.name

SPEC_TYPES = (
    ('int', _("integer")),
    ('float', _("float")),
    ('bool', _("boolean")),
    ('text', _("text")),
)

@python_2_unicode_compatible
class EntitySpec(models.Model):
    entity = models.ForeignKey(Entity)
    spectype = models.PositiveIntegerField(default=0)
    textvalue = models.TextField(max_length=200, default="", blank=True)
    intvalue = models.IntegerField(default=0)
    flotvalue = models.DecimalField(default=0, max_digits=10, decimal_places=3)
    boolvalue = models.BooleanField(default=False, blank=True)


class EntityGroupFamily(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    account = models.ForeignKey(Account)

    def __unicode__(self):
        return u"%s > %s" %(self.customer, self.title)

class EntityGroup(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    family = models.ForeignKey(EntityGroupFamily)
    entities = models.ManyToManyField(Entity)
    #option = generic.GenericRelation(Option)

    def __unicode__(self):
        return u"%s > %s" %(self.family, self.title)


class Unit(InfoDictModel):
    entity = models.ForeignKey(Entity)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    active = models.BooleanField(default=True)
    ref = models.ForeignKey('self', null=True, blank=True)
    class Meta:
        ordering = ('entity', 'name',)
        unique_together = ('entity', 'name')
        verbose_name = _('unit')

    def __unicode__(self):
        return self.name

#class UnitTree(MPTTModel):
#    parent = TreeForeignKey('self', related_name="children")
#    entity = models.ForeignKey(Entity)
#    name = models.CharField(max_length=100)
#    description = models.TextField(blank=True, default="")
#    active = models.BooleanField(default=True)
#    ref = models.ForeignKey('self', null=True, blank=True, related_name="refered")

class Activity(InfoDictModel):
    entity = models.ForeignKey(Entity)
    unit = models.ForeignKey(Unit, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    active = models.BooleanField(default=True)
    ref = models.ForeignKey('self', null=True, blank=True)
    equipments = models.ManyToManyField(Equipment, related_name="activity_equipments")

    class Meta:
        unique_together = ('entity', 'name')

