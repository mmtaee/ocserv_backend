from django.db import models


class Config(models.Model):
    captcha_site_key = models.TextField(null=True, blank=True)
    captcha_secret_key = models.TextField(null=True, blank=True)
    default_traffic = models.PositiveIntegerField(default=10)

    class Meta:
        db_table = "config"
