from django.urls import path
from .views import test_views


urlpatterns = [
    path('problemset/', test_views.show_list, name='problemset'),
]
