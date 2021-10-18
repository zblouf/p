# -*- coding: utf-8 -*-

from django.db import models
from z.org.entity.models import Activity
from z.prev.hazard.models import Hazard
from z.prev.action.models import Action
from z.prev.assess.models import Session
from z.meta.abstract.models import TrackedModel
from django.db.models.signals import pre_save
from django.dispatch import receiver


FREQUENCY_CHOICES = (
    (0, u'0'),
    (1, u'1'),
    (2, u'2'),
    (3, u'3'),
    (4, u'4'),
)

LETTER_CHOICES = (
    ('', u'[non coté]'),
    ('A', u'A : Toutes les mesures sont prises'),
    ('B', u'B : Les mesures sont partiellement prises'),
    ('C', u'C : Les mesures ne sont pas vraiment prises'),
    ('D', u"D : Aucune mesure n'est prise"),
    ('N', u'N :  Non applicable'),
)

CRIT_COEFFICIENTS = {
    '': 1,
    'N': 0,
    'A': 0.01,
    'B': 0.3,
    'C': 0.6,
    'D': 1,
}

class V1RiskAssessment(TrackedModel):
    session = models.ForeignKey(Session, null=True)
    activity = models.ForeignKey(Activity)
    hazard = models.ForeignKey(Hazard)
    comment = models.TextField(blank=True, default="")
    frequency = models.PositiveIntegerField(default=0, choices=FREQUENCY_CHOICES)
    collective_protection = models.CharField(max_length=2, blank=True, default="", choices=LETTER_CHOICES)
    individual_protection = models.CharField(max_length=2, blank=True, default="", choices=LETTER_CHOICES)
    training = models.CharField(max_length=2, blank=True, default="", choices=LETTER_CHOICES)
    information = models.CharField(max_length=2, blank=True, default="", choices=LETTER_CHOICES)
    # denormalized calculated fields
    raw_score = models.DecimalField(default=0, max_digits=8, decimal_places=3)
    weighted_score = models.DecimalField(default=0, max_digits=8, decimal_places=3)
    priority = models.PositiveIntegerField(default=0)
    
    archive_triggers = ['frequency', 'comment', 'collective_protection', 'individual_protection', 'training', 'information']

    class Meta:
        ordering = ['hazard']

    def calc_raw_score(self):
        self.raw_score = int(self.hazard.level) * int(self.frequency)
        return self.raw_score

    def calc_weighted_score(self):
        raw = self.calc_raw_score()
        _crit_count = 0
        crits = []
        _coeff = 1
        for c in ['collective_protection', 'individual_protection', 'information', 'training']:
            if getattr(self, c) in ['A', 'B', 'C', 'D', '']:
                crits.append(CRIT_COEFFICIENTS[getattr(self, c)])
        if len(crits)>0:
            v = 0
            for c in crits:
                v += c
            _coeff = v / len(crits)
        w = raw * _coeff
        self.weighted_score = w
        return w

    def calc_priority(self):
        pass

    def save(self, *args, **kwargs):
        self.calc_weighted_score()
        super(V1RiskAssessment, self).save(*args, **kwargs)

class V1RiskAssessmentHistory(models.Model):
    #timestamp = 
    assessment = models.ForeignKey(V1RiskAssessment, null=True)
    session = models.ForeignKey(Session, null=True)
    activity = models.ForeignKey(Activity)
    hazard = models.ForeignKey(Hazard)
    hazard_cause = models.TextField(blank=True ,default="")
    hazard_consequence = models.CharField(max_length=200, default="", blank=True)
    hazard_level = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True, default="")
    frequency = models.PositiveIntegerField(default=0, choices=FREQUENCY_CHOICES)
    collective_protection = models.CharField(max_length=2, blank=True, default="", choices=LETTER_CHOICES)
    individual_protection = models.CharField(max_length=2, blank=True, default="", choices=LETTER_CHOICES)
    training = models.CharField(max_length=2, blank=True, default="", choices=LETTER_CHOICES)
    information = models.CharField(max_length=2, blank=True, default="", choices=LETTER_CHOICES)
    # denormalized calculated fields
    raw_score = models.DecimalField(default=0, max_digits=8, decimal_places=3)
    weighted_score = models.DecimalField(default=0, max_digits=8, decimal_places=3)
    priority = models.PositiveIntegerField(default=0)


ACTION_STATUS_CHOICES = (
    (0, u'En place'),
    (1, u'A mener'),
)

class V1ActionTrack(models.Model):
    activity = models.ForeignKey(Activity)
    action = models.ForeignKey(Action)
    status = models.PositiveIntegerField(default=0, choices = ACTION_STATUS_CHOICES)
    responsible = models.CharField(max_length=100, blank=True, default="")
    deadline = models.DateField(null=True, blank=True)
    comment = models.TextField(blank=True)


@receiver(pre_save, sender=V1RiskAssessment)
def archive_v1_risk_assessment(sender, instance, **kwargs):
    if instance.pk:
        old = sender.objects.get(pk=instance.pk)
        _trigger = False
        for k in old.archive_triggers:
            if getattr(old, k)!=getattr(instance, k):
                _trigger = True
                break
        if _trigger:
            archive = V1RiskAssessmentHistory()
            archive.assessment = instance
            archive.session = old.session
            archive.activity = old.activity
            archive.hazard = old.hazard
            archive.hazard_cause = old.hazard.cause
            archive.hazard_consequence = old.hazard.consequence
            archive.hazard_level = old.hazard.level
            archive.comment = old.comment
            archive.frequency = old.frequency
            archive.collective_protection = old.collective_protection
            archive.individual_protection = old.individual_protection
            archive.training = old.training
            archive.information = old.information
            archive.raw_score = old.raw_score
            archive.weighted_score = old.weighted_score
            archive.priority = old.priority
            archive.save()