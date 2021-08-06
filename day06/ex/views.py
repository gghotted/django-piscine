import random
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout
from .forms import SignupForm, LoginForm, TipForm
from .models import User, Tip, addusers
from django.core.exceptions import PermissionDenied


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


class HomeView(generic.CreateView):
    template_name = 'ex/home.html'
    form_class = TipForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        kwargs['tips'] = addusers(Tip.objects.all(), self.request.user)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return redirect(reverse('login'))
        form.instance.author = self.request.user
        return super().form_valid(form)


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


class TipLikeView(generic.View):
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        tip = get_object_or_404(Tip, pk=pk)
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied('Not allowed user')

        # like 는 User.objects
        if tip.like.filter(username=user.username).exists():
            tip.like.remove(user)
        else:
            tip.like.add(user)
            tip.hate.remove(user)

        return redirect(reverse('home'))


class TipHateView(generic.View):
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        tip = get_object_or_404(Tip, pk=pk)
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied('Not allowed user')

        # hate 는 User.objects
        if tip.hate.filter(username=user.username).exists():
            tip.hate.remove(user)
        else:
            tip.hate.add(user)
            tip.like.remove(user)

        return redirect(reverse('home'))


class TipDeleteView(generic.DeleteView):
    model = Tip
    success_url = reverse_lazy('home')
    http_method_names = ['post']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        # https://heiswed.tistory.com/entry/%EC%9E%A5%EA%B3%A0Django-%EA%B0%9C%EB%B0%9C-%EA%B6%8C%ED%95%9Cpermission-%ED%99%94%EB%A9%B4-%EA%B4%80%EB%A6%AC
        obj.user = self.request.user
        if not obj.deleteable():
            raise PermissionDenied('Not allowed user')
        return obj
