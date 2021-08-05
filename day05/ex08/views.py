from io import StringIO
from django.views.generic import TemplateView
from django.conf import settings


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
    template_name = 'ex08/common.html'

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
        CREATE TABLE ex08_planets (
            id serial PRIMARY KEY,
            name varchar(64) NOT NULL UNIQUE,
            climate text,
            diameter integer,
            orbital_period integer,
            population bigint,
            rotation_period integer,
            surface_water real,
            terrain varchar(128)
        );
        CREATE TABLE ex08_people (
            id serial PRIMARY KEY,
            name varchar(64) NOT NULL UNIQUE,
            birth_year varchar(32),
            gender varchar(32),
            eye_color varchar(32),
            hair_color varchar(32),
            height integer,
            mass real,
            homeworld varchar(64),
            CONSTRAINT fk_homeworld FOREIGN KEY(homeworld) REFERENCES ex08_planets(name)
            ON DELETE SET NULL
        );
        '''
        self.excute(sql)


class PopulateView(DBManagerView):
    template_name = 'ex08/common.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            self.insert_rows()
            context['success'] = True
        except Exception as e:
            context['error_msg'] = str(e)
        return self.render_to_response(context)

    def insert_rows(self):
        with open(settings.BASE_DIR / 'ex08' / 'planets.csv', 'r') as f:
            self.cursor.copy_from(
                f,
                'ex08_planets',
                null='NULL',
                columns=(
                    'name',
                    'climate',
                    'diameter',
                    'orbital_period',
                    'population',
                    'rotation_period',
                    'surface_water',
                    'terrain',
                )
            )
        with open(settings.BASE_DIR / 'ex08' / 'people.csv', 'r') as f:
            self.cursor.copy_from(
                f,
                'ex08_people',
                null='NULL',
                columns=(
                    'name',
                    'birth_year',
                    'gender',
                    'eye_color',
                    'hair_color',
                    'height',
                    'mass',
                    'homeworld'
                )
            )
        self.connection.commit()


class DisplayView(DBManagerView):
    template_name = 'ex08/common.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            context['data'] = self.get_data()
            context['success'] = True
        except Exception as e:
            context['error_msg'] = str(e)
        return self.render_to_response(context)

    def get_data(self):
        sql = '''
        SELECT p.name, p.homeworld, world.climate as "world climate"
        FROM ex08_people as p
        INNER JOIN ex08_planets as world ON p.homeworld=world.name;
        '''
        rows = self.fatchall(sql)
        if len(rows) == 0:
            raise Exception('No data available')
        keys = self.cursor.description
        return {'keys':keys, 'rows':rows}
