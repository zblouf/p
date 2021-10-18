from django.db import models
from z.saas.models import Account
from z.meta.abstract.models import TrackedOwnedModel

class DocLink(TrackedOwnedModel):
	title = models.CharField(max_length=100)
	url = models.URLField()
	description = models.TextField(blank=True, default="")