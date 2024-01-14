from django.db import models


class DailyTaskChecking(models.Model):
    last_date = models.CharField(max_length=100, null=False, blank=False)
