from django.db import models

from user.models import Config


class OcservUser(models.Model):
    FREE = 1
    MONTHLY = 2
    TOTALLY = 3
    TRAFFIC_CHOICES = ((FREE, "free"), (MONTHLY, "monthly"), (TOTALLY, "totally"))
    group = models.CharField(max_length=64, default="defaults", unique=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32, null=True, blank=True)
    active = models.BooleanField(default=False)
    create = models.DateField(auto_now_add=True)
    expire_date = models.DateField(null=True, blank=True)
    deactivate_date = models.DateField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    traffic = models.PositiveSmallIntegerField(choices=TRAFFIC_CHOICES, default=MONTHLY)
    default_traffic = models.PositiveIntegerField(default=0)
    tx = models.DecimalField(max_digits=14, decimal_places=8, default=0)
    rx = models.DecimalField(max_digits=14, decimal_places=8, default=0)

    class Meta:
        db_table = "ocserv user"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.default_traffic and self.traffic != self.FREE:
                config = Config.objects.last()
                self.default_traffic = config.default_traffic
        if self.traffic != self.FREE and self.default_traffic < self.tx:
            self.active = False
        if self.traffic == self.FREE:
            self.default_traffic = 0
        # TODO: user handler
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # TODO: user handler
        super().delete(*args, **kwargs)


class MonthlyTrafficStat(models.Model):
    user = models.ForeignKey(OcservUser, on_delete=models.CASCADE, related_name="user")
    year = models.PositiveSmallIntegerField(default=2023)
    month = models.PositiveSmallIntegerField(default=1)
    tx = models.DecimalField(max_digits=14, decimal_places=8, default=0)
    rx = models.DecimalField(max_digits=14, decimal_places=8, default=0)

    class Meta:
        db_table = "monthly stats"

    def __str__(self):
        return f"{self.month} >> {self.tx}"
