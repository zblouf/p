from django.db import models
from z.saas.models import Account

class Session(models.Model):
    account = models.ForeignKey(Account)
    date_begin = models.DateField(null=True)
    date_end = models.DateField(null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")