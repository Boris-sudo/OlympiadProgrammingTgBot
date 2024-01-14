from django.db import models
from ..models import DailyTask


class DailyTaskSolvers(models.Model):
    task = models.ForeignKey(DailyTask, on_delete=models.CASCADE, null=True, blank=True)
