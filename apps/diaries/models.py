from django.db import models
from django.utils import timezone


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class Diary(models.Model):
    user = models.ForeignKey('users.User',
                             on_delete=models.CASCADE,
                             null=False,
                             blank=False)
    biceps = models.FloatField(null=True,
                               blank=True)
    forearm = models.FloatField(null=True,
                                blank=True)
    chest = models.FloatField(null=True,
                              blank=True)
    leg = models.FloatField(null=True,
                            blank=True)
    calves = models.FloatField(null=True,
                               blank=True)
    waist = models.FloatField(null=True,
                              blank=True)
    created_at = models.DateField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)
