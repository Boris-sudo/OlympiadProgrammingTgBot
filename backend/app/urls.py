from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views.tasks_views import problemset, daily_task
from .views.olympiads_view import get_olyampiads
from .views.topics_view import get_topics
from .views.login import login, create_account
from .views.register_player_to_fight import register, give_up_fight, check_fight, get_task, check_user_in_fight

urlpatterns = [
    path('codeforces/problemset/', problemset),
    path('codeforces/daily-task/', daily_task),

    path('olympiads/', get_olyampiads),
    path('topics/', get_topics),

    path('login/', login),
    path('create-account/', create_account),

    path('fight/', register),
    path('fight/give-up/', give_up_fight),
    path('fight/check/', check_fight),
    path('fight/task/', get_task),
    path('fight/exist/', check_user_in_fight),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
