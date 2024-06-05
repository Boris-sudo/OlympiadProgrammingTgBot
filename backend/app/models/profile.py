import random

from django.db import models
from .daily_task_solvers import DailyTaskSolvers


class Profile(models.Model):
    user_id = models.IntegerField(blank=False, null=False)
    rating = models.IntegerField(default=800, blank=True)
    codeforces_name = models.CharField(max_length=100, blank=False, null=False, default="")
    daily_solver = models.ForeignKey(DailyTaskSolvers, on_delete=models.CASCADE, blank=True, null=True)
    port = models.IntegerField(default=0)

    def __str__(self):
        return self.codeforces_name


class RatingChanges(models.Model):
    date = models.CharField(max_length=100, blank=False, null=False)
    rating = models.IntegerField(default=800, blank=False, null=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
