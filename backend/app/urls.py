from django.urls import path
from .views import test_views
from router import HybridRouter

router = HybridRouter()

router.add_api_view('login', )

urlpatterns = [
    path('problemset/', test_views.show_list, name='problemset'),

    path(),
]
