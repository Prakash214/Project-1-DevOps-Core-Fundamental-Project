from flask_testing import LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen
from flask import url_for
from application import app, db
from application.models import User
from application.forms import UserForm

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
        options = webdriver.chrome.options.Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(f'http://localhost:{self.TEST_PORT}/add-user')
    
    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
    
    def test_server_connectivity(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}/add-user')
        assert response.status == 200

class TestAddUser(TestBase):
    def submit_input(self, test_case):
        username_field = self.driver.find_element_by_xpath('/html/body/div/form/input[2]')
        submit = self.driver.find_element_by_xpath('/html/body/div/form/input[4]')
        username_field.send_keys(test_case[0])
        submit.click()
    
    def test_add_user(self):
        test_case = "prakasht"
        self.submit_input(test_case)
        assert list(User.query.all()) != []
        assert User.query.filter_by(username="prakasht").first() is not None
    
    def test_add_user_validation(self):
        test_case = "prakash214"
        self.submit_input(test_case)
        assert list(User.query.all()) == []
        assert User.query.filter_by(username="prakash214").first() is None