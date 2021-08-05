from django.urls import path
from .views import *


urlpatterns = [
    path('display', DisplayView.as_view())
]

