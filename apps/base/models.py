from django.db import models

from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    protocol = models.CharField(max_length=5,
                                help_text=
                                "Protocol to access the site e.g. 'http'")
    domain = models.CharField(max_length=255,
                              help_text="Site domain e.g. 'api.diary.com")
    title = models.CharField(max_length=255,
                             null=False,
                             blank=True,
                             default='Diary Api')

    class Meta:
        verbose_name = "Site Configuration"

    @classmethod
    def get_solo(cls):
        super(SiteConfiguration, cls).get_solo()
        obj, created = cls.objects.get_or_create(pk=cls.singleton_instance_id)
        return obj

    def __str__(self):
        return f"Site Configuration {self.title}"
