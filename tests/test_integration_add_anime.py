from flask_testing import LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen
from flask import url_for
from application import app, db
from application.models import *
from application.forms import *
from datetime import date, timedelta

class TestBase(LiveServerTestCase):
    TEST_PORT = 5050

    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'sqlite:///testdb.db',
            LIVESERVER_PORT = self.TEST_PORT,
            DEBUG = True,
            TESTING = True
        )

        return app
    
    def setUp(self):
        db.create_all()
        sample_user = User(username="Prakash")
        db.session.add(sample_user)
        db.session.commit()
        options = webdriver.chrome.options.Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(f'http://localhost:{self.TEST_PORT}/add-anime')

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
    
    def test_server_connectivity(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}/add-anime')
        assert response.status == 200

class TestAddUser(TestBase):
    def submit_input(self, test_case, test_valid = False):
        anime_name_field = self.driver.find_element_by_xpath('/html/body/div/form/input[2]')
        anime_desc_field = self.driver.find_element_by_xpath('/html/body/div/form/textarea')
        date_field = self.driver.find_element_by_xpath('/html/body/div/form/input[3]')
        status_field = self.driver.find_element_by_xpath('/html/body/div/form/select[1]')
        assigned_to_field = self.driver.find_element_by_xpath('/html/body/div/form/select[2]')
        submit = self.driver.find_element_by_xpath('/html/body/div/form/input[4]')
        anime_name_field.send_keys(test_case[0])
        anime_desc_field.send_keys(test_case[1])
        if test_valid:
            date_field.clear()
        status_field.send_keys(test_case[2])
        assigned_to_field.send_keys(test_case[3])
        submit.click()
    
    def test_add_task(self):
        test_case = "Sample Anime", "A task for the integration test", 'done', 'Prakash'
        self.submit_input(test_case)
        assert list(Anime.query.all()) != []
        assert Anime.query.filter_by(anime_name="Sample Anime").first() is not None