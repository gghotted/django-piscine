from django.urls import path
from .views import random_name_view, HomeView, SignupView, LoginView, LogoutView


urlpatterns = [
    path('', random_name_view),
    path('home', HomeView.as_view(), name='home'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
