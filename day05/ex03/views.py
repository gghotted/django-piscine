from django.views.generic import TemplateView
from .models import Movies

class PopulateView(TemplateView):
    template_name = 'ex02/common.html'

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
            '''
            Movies(**row).save()
            이 방법은 같은 데이터를 가진 row가 있다면 그 row에 해당하는 객체를 생성
            즉 이미 존재하는 row를 업데이트함.
            따라서 primary_key가 중복되어도 raise하지 않음.
            '''
            Movies.objects.create(**row)


class DisplayView(TemplateView):
    template_name = 'ex02/common.html'

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
