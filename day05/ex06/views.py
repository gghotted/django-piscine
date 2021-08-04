from django.shortcuts import render
from django.views.generic import TemplateView, View
import psycopg2


class DBManagerView(TemplateView):
    user = 'djangouser'
    password = 'secret'
    database = 'djangotraining'

    def excute(self, sql, commit=True):
        self.cursor.execute(sql)
        if commit:
            self.connection.commit()

    def fatchall(self, sql):
        self.excute(sql, commit=False)
        return self.cursor.fetchall()

    def dispatch(self, request, *args, **kwargs):
        self.connection = psycopg2.connect(
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return super().dispatch(request, *args, **kwargs)


class InitView(DBManagerView):
    template_name = 'ex06/common.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            self.init_table()
            context['success'] = True
        except Exception as e:
            context['error_msg'] = str(e)
        return self.render_to_response(context)

    def init_table(self):
        sql = '''
        CREATE TABLE ex06_movies (
            title varchar(64) UNIQUE NOT NULL,
            episode_nb integer PRIMARY KEY,
            opening_crawl text,
            director varchar(32) NOT NULL,
            producer varchar(128) NOT NULL,
            release_date date NOT NULL,
            created timestamp,
            updated timestamp
        );

        CREATE OR REPLACE FUNCTION update_changetimestamp_column()
        RETURNS TRIGGER AS $$
        BEGIN
        NEW.updated = now();
        NEW.created = OLD.created;
        RETURN NEW;
        END;
        $$ language 'plpgsql';
        CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
        ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
        update_changetimestamp_column();

        CREATE OR REPLACE FUNCTION create_timestamp_column()
        RETURNS TRIGGER AS $$
        BEGIN
        NEW.updated = now();
        NEW.created = now();
        RETURN NEW;
        END;
        $$ language 'plpgsql';
        CREATE TRIGGER create_films_changetimestamp BEFORE INSERT
        ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
        create_timestamp_column();
        '''
        self.excute(sql)


class PopulateView(DBManagerView):
    template_name = 'ex06/common.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            self.insert_rows()
            context['success'] = True
        except Exception as e:
            context['error_msg'] = str(e)
        return self.render_to_response(context)

    def insert_rows(self):
        sql = '''
        INSERT INTO ex06_movies(episode_nb, title, director, producer, release_date)
        VALUES({episode_nb}, '{title}', '{director}', '{producer}', '{release_date}')
        '''
        rows = [
            {
                "episode_nb": "1",
                "title": "The Phantom Menace",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "1999-05-19"
            },
            {
                "episode_nb": "2",
                "title": "Attack of the Clones",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "2002-05-16"
            },
            {
                "episode_nb": "3",
                "title": "Revenge of the Sith",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "2005-05-19"
            },
            {
                "episode_nb": "4",
                "title": "A New Hope",
                "director": "George Lucas",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1977-05-25"
            },
            {
                "episode_nb": "5",
                "title": "The Empire Strikes Back",
                "director": "Irvin Kershner",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1980-05-17"
            },
            {
                "episode_nb": "6",
                "title": "Return of the Jedi",
                "director": "Richard Marquand",
                "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
                "release_date": "1983-05-25"
            },
            {
                "episode_nb": "7",
                "title": "The Force Awakens",
                "director": "J. J. Abrams",
                "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
                "release_date": "2015-12-11"
            }
        ]
        for row in rows:
            self.excute(sql.format(**row), commit=True)


class DisplayView(DBManagerView):
    template_name = 'ex06/common.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            context['data'] = self.get_data()
            context['success'] = True
        except Exception as e:
            context['error_msg'] = str(e)
        return self.render_to_response(context)

    def get_data(self):
        sql = ' SELECT * FROM ex06_movies'
        rows = self.fatchall(sql)
        if len(rows) == 0:
            raise Exception('No data available')
        keys = self.cursor.description
        return {'keys':keys, 'rows':rows}


class UpdateView(DBManagerView, View):
    template_name = 'ex06/update.html'

    def get(self, request):
        context = {
            'titles': self.get_titles()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        try:
            self.update(request.POST['title'], request.POST['opening_crawl'])
            context['success'] = True
        except Exception as e:
            context['error_msg'] = 'No data available'
        context['titles'] = self.get_titles()
        return render(request, self.template_name, context)

    def update(self, title, opening_crawl):
        sql = f"UPDATE ex06_movies SET opening_crawl='{opening_crawl}' Where title='{title}'"
        self.excute(sql)

    def get_titles(self):
        sql = ' SELECT title FROM ex06_movies'
        titles = map(lambda tup: tup[0], self.fatchall(sql))
        return titles
