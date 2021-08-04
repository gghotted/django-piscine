from django.urls import path
from .views import *


urlpatterns = [
    path('init', InitView.as_view()),
    path('populate', PopulateView.as_view()),
    path('display', DisplayView.as_view()),
    path('remove', RemoveView.as_view())
]
