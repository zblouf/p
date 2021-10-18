from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from z.saas.models import Account
from z.prev.domain.models import Domain
from z.meta.abstract.models import DocModel, TrackedOwnedModel

HAZARD_LEVEL_CHOICES = (
    (   1, _(u'minor injury')), # blessure légère sans AT
    (  10, _(u'sick leave')), # arrêt de travail
    ( 100, _(u'permanent disability')), # incapacité permanente
    (1000, _(u'fatal')), # mortel
)

ILO_DRAFT_CLASSIFICATION = (
    (1, _(u'Accident')),
    (2, _(u'Physical')),
    (3, _(u'Chemical')),
    (4, _(u'Biological')),
    (5, _(u'Ergonomic')),
    (6, _(u'Psychological')),
    (7, _(u'Organisational')),
    (8, _(u'Other')),
)

# Could be deprecated soon
INRS_ED840_DOMAINS = (
    ( 0, _('[non défini]')),
    ( 1, _('Accident de plain-pied')),
    ( 2, _('Chute de hauteur')),
    ( 3, _('Circulations internes')),
    ( 4, _('Risque routier')),
    ( 5, _('Activité physique')),
    ( 6, _('Manutention mécanique')),
    ( 7, _('Produits, émissions et déchets')),
    ( 8, _('Agents biologiques')),
    ( 9, _('Equipements de travail')),
    (10, _('Effondrements et chutes d\'objets')),
    (11, _('Bruit')),
    (12, _('Ambiances thermiques')),
    (13, _('Incendie, explosion')),
    (14, _('Electricité')),
    (15, _('Eclairage')),
    (16, _('Rayonnements')),
    (17, _('Autres')),
)

class Hazard(TrackedOwnedModel, DocModel):
    domain = models.ForeignKey(Domain)
    deprecated = models.BooleanField(default=False)
    cause = models.TextField()
    consequence = models.TextField()
    level = models.PositiveIntegerField(default=1, choices=HAZARD_LEVEL_CHOICES)
    comment = models.TextField(blank=True, default="")
#    ed840_domain = models.PositiveIntegerField(default=0, choices=INRS_ED840_DOMAINS)

    class Meta:
        ordering = ['domain', 'cause']

    def __unicode__(self):
        return self.cause