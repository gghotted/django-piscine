from django.views.generic import TemplateView
from django.conf import settings
from .models import People


class DisplayView(TemplateView):
    template_name = 'ex09/display.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            context['objects'] = self.get_data()
            context['success'] = True
        except Exception as e:
            context['error_msg'] = str(e)
        return self.render_to_response(context)

    def get_data(self):
        objects = People.objects.all()
        if not People.objects.exists():
            raise Exception(
                'No data available, please use the following command line before use:\n' \
                'python manage.py loaddata ex09/ex09_initial_data.json'
            )
        return objects
