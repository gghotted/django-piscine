from django.urls import path
from .views import random_name_view


urlpatterns = [
    path('', random_name_view)
]
