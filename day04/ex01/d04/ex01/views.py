from django.shortcuts import render
from django.views.generic import TemplateView


class DjangoView(TemplateView):
    template_name = 'ex01/django.html'


class DisplayView(TemplateView):
    template_name = 'ex01/display.html'


class TemplatesView(TemplateView):
    template_name = 'ex01/templates.html'
