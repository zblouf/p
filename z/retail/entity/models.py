from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from z.org.entity.models import Entity

DISCOUNT_TYPE_CHOICES = (
    (0, _('none')),
    (1, _('fixed price')),
    (2, _('percentage')),
    (3, _('value')),
)

@python_2_unicode_compatible
class SalesEntityExt(models.Model):
    entity = models.OneToOneField(Entity)
    is_charged = models.BooleanField(default=True)
    discount_type = models.PositiveIntegerField(default=0, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    comment = models.TextField(blank=True, default="")
    
    def __str__(self):
        return "%s [%s]" %(self.entity, str(self.is_charged))
