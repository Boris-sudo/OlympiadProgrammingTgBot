from django.contrib.auth.models import User
from django.db import models


class DailyTask(models.Model):
    rating = models.IntegerField(blank=False, null=False, default=0, verbose_name="rating of the task")
    date = models.CharField(max_length=1000, blank=False, null=False, verbose_name="date of the task")
    contestId = models.IntegerField(blank=False, null=False, verbose_name='contest id')
    index = models.CharField(max_length=10, blank=False, null=False, verbose_name='index of the task')
