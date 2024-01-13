from django.contrib import admin

from .models import DailyTask, Profile, RatingChanges

admin.site.register(DailyTask)
admin.site.register(Profile)
admin.site.register(RatingChanges)
