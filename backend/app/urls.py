from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views.codeforces_views import problemset, daily_task
from .views.olympiads import get_olyampiads

urlpatterns = [
    path('codeforces/problemset/', problemset),
    path('codeforces/daily-task/', daily_task),

    path('olympiads/', get_olyampiads),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
