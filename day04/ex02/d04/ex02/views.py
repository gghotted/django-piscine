from django.shortcuts import render
from django.views.generic import FormView
from .forms import IndexForm
from django.conf import settings
from django.utils.datetime_safe import datetime


class IndexView(FormView):
    template_name = 'ex02/index.html'
    form_class = IndexForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history'] = self.get_history()
        return context

    def get_history(self):
        try:
            with open(settings.EX02_LOGS_PATH, 'r') as f:
                return f.read()
        except:
            return ''

    def append_history(self, msg):
        with open(settings.EX02_LOGS_PATH, 'a') as f:
            timestamp = str(datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'
            ))
            f.write(timestamp + ': ' + msg + '\n')

    def form_valid(self, form):
        self.append_history(form.cleaned_data['msg'])
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path
