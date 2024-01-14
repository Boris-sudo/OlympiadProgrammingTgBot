from django.contrib import admin

from .models import *

admin.site.register(DailyTask)
admin.site.register(Profile)
admin.site.register(RatingChanges)
admin.site.register(DailyTaskSolvers)
