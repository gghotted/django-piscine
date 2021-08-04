from django.shortcuts import render
from django.views.generic import TemplateView, View
from .models import Movies


class PopulateView(TemplateView):
    template_name = 'ex07/common.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            self.insert_rows()
            context['success'] = True
        except Exception as e:
            context['error_msg'] = str(e)
        return self.render_to_response(context)

    def insert_rows(self):
        rows = [
            {
                "episode_nb": 1,
                "title": "The Phantom Menace",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "1999-05-19"
            },
            {
                "episode_nb": 2,
                "title": "Attack of the Clones",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "2002-05-16"
            },
            {
                "episode_nb": 3,
                "title": "Revenge of the Sith",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "2005-05-19"
            },
            {
                "episode_nb": 4,
                "title": "A New Hope",
                "director": "George Lucas",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1977-05-25"
            },
            {
                "episode_nb": 5,
                "title": "The Empire Strikes Back",
                "director": "Irvin Kershner",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1980-05-17"
            },
            {
                "episode_nb": 6,
                "title": "Return of the Jedi",
                "director": "Richard Marquand",
                "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
                "release_date": "1983-05-25"
            },
            {
                "episode_nb": 7,
                "title": "The Force Awakens",
                "director": "J. J. Abrams",
                "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
                "release_date": "2015-12-11"
            }
        ]
        for row in rows:
            Movies.objects.create(**row)


class DisplayView(TemplateView):
    template_name = 'ex07/common.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            context['data'] = self.get_data()
            context['success'] = True
        except Exception as e:
            context['error_msg'] = str(e)
        return self.render_to_response(context)

    def get_data(self):
        if not Movies.objects.all().exists():
            raise Exception('No data available')
        return {'keys': Movies._meta.fields, 'rows': Movies.objects.values_list()}


class UpdateView(View):
    template_name = 'ex07/update.html'

    def get(self, request):
        context = {
            'titles': self.get_titles()
        }
        if not Movies.objects.exists():
            context['error_msg'] = 'No data available'
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        try:
            obj = Movies.objects.get(title=request.POST['title'])
            obj.opening_crawl = request.POST['opening_crawl']
            obj.save()
            context['success'] = True
        except Exception as e:
            context['error_msg'] = 'No data available'
        context['titles'] = self.get_titles()
        return render(request, self.template_name, context)

    def get_titles(self):
        return map(lambda tup: tup[0], Movies.objects.values_list('title'))

