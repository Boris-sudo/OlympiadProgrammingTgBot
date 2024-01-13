from django.db import models


class RatingChanges(models.Model):
    date = models.CharField(max_length=100, blank=False, null=False)
    rating = models.IntegerField(default=800, blank=False, null=False)


class Profile(models.Model):
    user_id = models.IntegerField(blank=False, null=False)
    rating = models.IntegerField(default=800, blank=True)
    rating_changes = models.ManyToManyField(RatingChanges, blank=True)
    codeforces_name = models.CharField(max_length=100, blank=False, null=False, default="")
