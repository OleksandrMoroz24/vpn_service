from django.db import models
from django.conf import settings


class UserSite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f"{self.name} - {self.url}"


class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site_url = models.URLField()
    page_transitions = models.PositiveIntegerField(default=0)
    data_uploaded = models.PositiveIntegerField(default=0)
    data_downloaded = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.site_url}"
