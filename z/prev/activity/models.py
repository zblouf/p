from django.db import models
from z.org.entity.models import Activity
from z.prev.profile.models import Profile
from z.means.equipment.models import Equipment
from jsonfield import JSONField

class PrevActivityExt(models.Model):
    activity = models.OneToOneField(Activity)
    profile = models.ForeignKey(Profile, blank=True, null=True)
    prev_comment = models.TextField(blank=True, default="")
    equipments = models.ManyToManyField(Equipment, related_name="equipments")

    info = JSONField(blank=True, default={})

    # Denormalized fields (for statistics display)
    

    def __str__(self):
        return u"[ext|prev] %s" %(self.activity)
