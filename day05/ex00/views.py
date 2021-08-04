from django.views.generic import TemplateView
import psycopg2


class InitView(TemplateView):
    template_name = 'ex00/init.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            self.init_table()
            context['success'] = True
        except Exception as e:
            context['error_msg'] = str(e)
        return self.render_to_response(context)

    def init_table(self):
        params = {
            'user': 'djangouser',
            'password': 'secret',
            'database': 'djangotraining',
        }
        sql = '''
        CREATE TABLE ex00_movies (
            title varchar(64) UNIQUE NOT NULL,
            episode_nb integer PRIMARY KEY,
            opening_crawl text,
            director varchar(32) NOT NULL,
            producer varchar(128) NOT NULL,
            release_date date NOT NULL
        )
        '''
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()


