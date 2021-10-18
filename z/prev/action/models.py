from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from z.saas.models import Account
from z.prev.domain.models import Domain
from z.meta.abstract.models import DocModel, TrackedOwnedModel

PERIOD_UNIT_CHOICES = (
    ('_', _(u'_')),
    ('y', _(u'year')),
    ('m', _(u'month')),
    ('w', _(u'week')),
    ('d', _(u'day')),
)

@python_2_unicode_compatible
class ActionType(TrackedOwnedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Action(DocModel, TrackedOwnedModel):
    domain = models.ForeignKey(Domain)
    type = models.ForeignKey(ActionType, blank=True, null=True)
    deprecated = models.BooleanField(default=False)
    caption_todo = models.TextField()
    caption_done = models.TextField()
    danger_consequence = models.TextField()
    comment = models.TextField(blank=True, default="")
    is_periodic = models.BooleanField(default=False)
    period_unit = models.CharField(max_length=2, default="_", choices=PERIOD_UNIT_CHOICES)
    period_value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.caption_todo
