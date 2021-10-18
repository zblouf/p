from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from z.saas.models import Account
from z.meta.abstract.models import DocModel, TrackedOwnedModel
from z.prev.domain.models import Domain
from z.prev.hazard.models import Hazard
from z.prev.action.models import Action

Z_PREV_PROFILETYPE_DOMAIN = 1
Z_PREV_PROFILETYPE_HAZARD = 2
Z_PREV_PROFILETYPE_HAZARDACTION = 3

PROFILE_TYPE_CHOICES = (
    (Z_PREV_PROFILETYPE_DOMAIN , 
        _('by domains')),
    (Z_PREV_PROFILETYPE_HAZARD, 
        _('by hazards')),
    (Z_PREV_PROFILETYPE_HAZARDACTION, 
        _('by hazards and actions')),
)

@python_2_unicode_compatible
class Profile(DocModel, TrackedOwnedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    type = models.PositiveIntegerField(default=0, choices=PROFILE_TYPE_CHOICES)
    # Associations
    domains = models.ManyToManyField(Domain, through="ProfileDomain")
    hazards = models.ManyToManyField(Hazard, through="ProfileHazard")
    actions = models.ManyToManyField(Action, through="ProfileAction")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_domains(self):
        domains = []
        if self.type == Z_PREV_PROFILETYPE_DOMAIN:
            domains = self.domains.all()
        elif self.type == Z_PREV_PROFILETYPE_HAZARD:
            domains = Domain.objects.filter(id__in=self.hazards.values_list('domain'))
        elif self.type == Z_PREV_PROFILETYPE_HAZARDACTION:
            domains = []
        return domains

    def get_hazards(self):
        hazards = []
        if self.type == G_PREV_PROFILETYPE_DOMAIN:
            hazards = Hazard.objects.filter(domain__in=self.domains.all()).order_by('domain', 'cause')
        elif self.type == G_PREV_PROFILETYPE_HAZARD \
                or self.type == G_PREV_PROFILETYPE_HAZARDACTION:
            hazards = self.hazards.all().order_by('domain', 'cause')
        return hazards

    def get_actions(self):
        actions = []
        if self.type == G_PREV_PROFILETYPE_DOMAIN:
            actions = Action.objects.filter(domain__in=self.domains.all())
        elif self.type == G_PREV_PROFILETYPE_HAZARD:
            # todo : write the actual code
            actions = Action.objects.filter(domain_id__in=self.hazards.values_list('domain', flat=True))
        elif self.type == G_PREV_PROFILETYPE_HAZARDACTION:
            self.actions.all()
        return actions

@python_2_unicode_compatible
class ProfileDomain(models.Model):
    profile = models.ForeignKey(Profile)
    domain = models.ForeignKey(Domain)
    forced = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    comment = models.TextField(blank=True, default='')

@python_2_unicode_compatible
class ProfileHazard(models.Model):
    profile = models.ForeignKey(Profile)
    hazard = models.ForeignKey(Hazard)
    forced = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    comment = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['hazard']

@python_2_unicode_compatible
class ProfileAction(models.Model):
    profile = models.ForeignKey(Profile)
    action = models.ForeignKey(Action)
    forced = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    comment = models.TextField(blank=True, default='')
