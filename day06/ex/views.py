import random
from django.shortcuts import render, redirect
from django.conf import settings
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from .forms import SignupForm, LoginForm
from .models import User


def random_name_view(request):
    if request.user.is_authenticated:
        if request.session.get_expiry_age() != 1209600:
            request.session.set_expiry(1209600) # defalut: two weeks
    else:
        request.session.setdefault('name', get_random_name())
        if request.session.get_expiry_age() != 3:
            request.session.set_expiry(3)
    return render(request, 'ex/random_name.html')


def get_random_name():
    return random.sample(settings.RANDOM_NAMES, 1)[0]


class HomeView(generic.TemplateView):
    template_name = 'ex/home.html'


class SignupView(generic.CreateView):
    template_name = 'ex/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        ret = super().form_valid(form)
        login(self.request, self.object)
        self.request.session.set_expiry(1209600)
        return ret


class LoginView(generic.FormView):
    template_name = 'ex/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        login(self.request, User.objects.get(username=username))
        self.request.session.set_expiry(1209600)
        return super().form_valid(form)


class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home'))


