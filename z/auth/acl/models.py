from django.db import models
from django.contrib.auth.models import User
from z.saas.models import Account
from z.org.entity.models import Entity
from z.core.app.models import App
from django.utils.translation import ugettext_lazy as _

ACL_ENTITY_MODE_GLOBAL = 1
ACL_ENTITY_MODE_DETAIL = 2

ENTITY_ACL_MODE_CHOICES = (
    (ACL_ENTITY_MODE_GLOBAL, _('global')),
    (ACL_ENTITY_MODE_DETAIL, _('detail')),
)

class EntityACL(models.Model):
    entity = models.ForeignKey(Entity)
    user = models.ForeignKey(User)
    can_view = models.BooleanField(default=False)
    can_modify = models.BooleanField(default=False)
    mode = models.PositiveIntegerField( default=ACL_ENTITY_MODE_GLOBAL,
                                        choices=ENTITY_ACL_MODE_CHOICES)
    detail_apps = models.BooleanField(default=False)
#    modules = models.ManyToManyField(Module)

    def __unicode__(self):
        perms = "|"
        if self.can_view:
            perms += "view|"
        if self.can_modify:
            perms += "modify|"
        return "%s for %s (%s)" %(self.user.zuser.clean_username, self.entity, perms)

#class AppEntity(models.Model):
    