from django.urls import path
from ex01.views import DjangoView, DisplayView, TemplatesView

app_name = 'ex01'
urlpatterns = [
    path('django', DjangoView.as_view(), name='django'),
    path('display', DisplayView.as_view(), name='display'),
    path('templates', TemplatesView.as_view(), name='templates')
]
