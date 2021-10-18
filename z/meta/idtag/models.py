from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class IdTag(models.Model):
    label = models.CharField(max_length=100, default="GV1_ID")
    value = models.PositiveIntegerField(default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') 

    def __unicode__(self):
        return "%s : %s" %(self.label, self.value)
