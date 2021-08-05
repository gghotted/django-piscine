from django.shortcuts import render
from django.conf import settings
import random


def random_name_view(request):
    request.session.setdefault('name', get_random_name())
    return render(request, 'ex/random_name.html')


def get_random_name():
    return random.sample(settings.RANDOM_NAMES, 1)[0]
