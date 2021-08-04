from django.urls import path
from .views import *


urlpatterns = [
    path('populate', PopulateView.as_view()),
    path('display', DisplayView.as_view()),
    path('update', UpdateView.as_view())
]
