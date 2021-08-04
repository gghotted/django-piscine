from django.urls import path
from .views import *


urlpatterns = [
    path('init', InitView.as_view())
]
