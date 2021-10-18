from django.db import models
from z.meta.abstract.models import TrackedOwnedModel
from django.utils.translation import ugettext_lazy as _

EQUIPMENT_TYPE_CHOICES = (
    (0, _('undefined')),
    (1, _('individual')),
    (2, _('collecive')),
)

class Equipment(TrackedOwnedModel):
#    customer = models.ForeignKey(Customer)
#    is_public = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    type = models.PositiveIntegerField(choices=EQUIPMENT_TYPE_CHOICES, default=0)

    def __str__(self):
        return self.name
