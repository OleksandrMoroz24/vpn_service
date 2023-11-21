from django.db import models
from django.conf import settings


class UserSite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"{self.name} - {self.url}"


class VpnUsageStatistics(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site_url = models.URLField()
    page_transitions = models.IntegerField(default=0)
    data_sent = models.BigIntegerField(default=0)  # in bytes
    data_received = models.BigIntegerField(default=0)  # in bytes

    def __str__(self):
        return f"{self.user.username} - {self.site_url}"
