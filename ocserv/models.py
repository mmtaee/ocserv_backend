from django.db import models

from user.models import Config


class OcservUser(models.Model):

    class TrafficChoices(models.IntegerChoices):
        FREE = 1, "free"
        MONTHLY = 2, "monthly"
        TOTALLY = 3, "totally"

    group = models.CharField(max_length=64, default="defaults")
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32, null=True, blank=True)
    lock = models.BooleanField(default=False)
    create = models.DateField(auto_now_add=True)
    expire_date = models.DateField(null=True, blank=True)
    deactivate_date = models.DateField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    traffic = models.PositiveSmallIntegerField(
        choices=TrafficChoices.choices, default=TrafficChoices.FREE
    )
    default_traffic = models.PositiveIntegerField(default=0)
    tx = models.DecimalField(max_digits=14, decimal_places=8, default=0)
    rx = models.DecimalField(max_digits=14, decimal_places=8, default=0)

    class Meta:
        db_table = "ocserv user"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.default_traffic and self.traffic != self.TrafficChoices.FREE:
                config = Config.objects.last()
                self.default_traffic = config.default_traffic
        if self.traffic != self.TrafficChoices.FREE and self.default_traffic < self.tx:
            self.lock = True
        if self.traffic == self.TrafficChoices.FREE:
            self.default_traffic = 0
        super().save(*args, **kwargs)


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
