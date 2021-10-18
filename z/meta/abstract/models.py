from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from jsonfield import JSONField
from z.saas.models import Account

@python_2_unicode_compatible
class MiscDictModel(models.Model):
    misc = JSONField()

    class Meta:
        abstract = True

@python_2_unicode_compatible
class InfoDictModel(models.Model):
    info = JSONField(blank=True, default={})

    class Meta:
        abstract = True

    def get_info(self, key):
        pass

    def set_info(self, key, value):
        pass


@python_2_unicode_compatible
class TrackedOwnedModel(models.Model):
    account = models.ForeignKey(Account, related_name="%(app_label)s_%(class)s_owned_by")
    shared = models.BooleanField(default=False)
    creation_timestamp = models.DateTimeField(blank=True)
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created_by", null=True, blank=True)
    modification_timestamp = models.DateTimeField(blank=True)
    modified_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modified_by", null=True, blank=True)
    user = False

    class Meta:
        abstract = True

    def set_user(self, user):
        self.user = user

    def save(self, *args, **kwargs):
        if self.id is None:
            if self.user:
                self.created_by = self.user
            self.creation_timestamp = timezone.now()
        if self.user:
            self.modified_by = self.user
        else:
            self.modified_by = None
        self.modification_timestamp = timezone.now()
        super(TrackedOwnedModel, self).save(*args, **kwargs)

@python_2_unicode_compatible
class TrackedModel(models.Model):
    creation_timestamp = models.DateTimeField(blank=True)
    created_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created_by", null=True, blank=True)
    modification_timestamp = models.DateTimeField(blank=True)
    modified_by = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_modified_by", null=True, blank=True)
    user = False

    class Meta:
        abstract = True

    def set_user(self, user):
        self.user = user

    def save(self, *args, **kwargs):
        if self.id is None:
            if self.user:
                self.created_by = self.user
            self.creation_timestamp = timezone.now()
        if self.user:
            self.modified_by = self.user
        else:
            self.modified_by = None
        self.modification_timestamp = timezone.now()
        super(TrackedModel, self).save(*args, **kwargs)

@python_2_unicode_compatible
class DocModel(models.Model):
    docs = models.ManyToManyField("file.DocFile", related_name="%(app_label)s_%(class)s_docs")
    links = models.ManyToManyField("link.DocLink", related_name="%(app_label)s_%(class)s_links")

    class Meta:
        abstract = True
