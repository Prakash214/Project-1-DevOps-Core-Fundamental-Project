from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from application import app, db
from application.models import *
from flask_testing import TestCase
from datetime import date, timedelta


class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///testdb.db',
            WTF_CSRF_ENABLED = False,
            DEBUG = True,
            SECRET_KEY = 'ASD ASD AS'
        )

        return app

    def setUp(self):
        db.create_all()
        user1=User(username ='Sample')
        anime1 = Anime(anime_name = 'Sample Anime', anime_desc = 'this that this that', anime_status = 'done', released_date= date.today() + timedelta(30), assigned_to = 1)
        db.session.add(user1)   
        db.session.add(anime1)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestHomeView(TestBase):
    def test_get_home(self):
        response = self.client.get(url_for('index'))
        self.assert200(response)
        self.assertIn(b'Anime list', response.data)

    def test_get_users(self):
        response = self.client.get(url_for('view_all_users'))
        self.assert200(response)
        self.assertIn(b'Sample', response.data)

    def test_get_anime(self):
        response = self.client.get(url_for('view_all_animes'))
        self.assert200(response)
        self.assertIn(b'Sample Anime', response.data)
        self.assertIn(b'Sample', response.data)

    def test_get_add_u(self):
        response = self.client.get(url_for('add_user'))
        self.assert200(response)
        self.assertIn(b'Username', response.data)
    
    def test_get_add_a(self):
        response = self.client.get(url_for('add_new_anime'))
        self.assert200(response)
        self.assertIn(b'Anime Name', response.data)
    
    def test_get_update_u(self):
        response = self.client.get(url_for('update_user', id=1))
        self.assert200(response)
        self.assertIn(b'Username', response.data)
    
    def test_get_update_a(self):
        response = self.client.get(url_for('update_anime', id=1))
        self.assert200(response)
        self.assertIn(b'Anime Name', response.data)
    
    def test_get_delete_u(self):
        response = self.client.get(
            url_for('delete_user', id=1),
            follow_redirects = True
        )
        self.assert200(response)
        self.assertNotIn(b'Sample', response.data)

    def test_get_delete_a(self):
        response = self.client.get(
            url_for('delete_anime', id=1),
            follow_redirects = True
        )
        self.assert200(response)
        self.assertNotIn(b'Sample Anime', response.data)

class TestPostRequests(TestBase):
    def test_post_add_u(self):
        response = self.client.post(
            url_for('add_user'),
            data = dict(username = 'prakash'),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'prakash', response.data)
        #assert User.query.filter_by(username='prakash').first() is not None

    def test_post_update_u(self):
        response = self.client.post(
            url_for('update_user', id=1),
            data = dict(username='New'),
            follow_redirects=True
        )

        self.assert200(response)
        assert User.query.filter_by(username='New').first() is not None
        assert User.query.filter_by(username='Sample').first() is None
    
    def test_post_add_a(self):                 
        response = self.client.post(
            url_for('add_new_anime'),
            data = dict(
                anime_name = 'Another Sample', 
                anime_desc='Yet another sample anime', 
                anime_status='done', 
                released_date = date.today() + timedelta(30), 
                assigned_to=1
                ),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'Another Sample', response.data)
    
    def test_post_update_a(self):
        response = self.client.post(
            url_for('update_anime', id=1),
            data = dict(
                anime_name ='Updated Name',
                anime_desc='New description of anime',
                anime_status='finished', 
                released_date = date.today() + timedelta(14), 
                assigned_to=1
                ),
            follow_redirects = True
        )
        self.assert200(response)
        #self.assertIn(b'finished', response.data)
        assert Anime.query.filter_by(anime_name='Updated Name').first() is not None
        assert Anime.query.filter_by(anime_name='Anime Name').first() is None