import unittest
import time
from flask import url_for
from urllib.request import urlopen
from os import getenv
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from app import app, db
from app.models import User, Stock, Supplier
import os

# setting the test variables for test admin user
test_admin_first_name =  "admin"
test_admin_last_name = "admin"
test_admin_email = "admin@admin.com"
test_admin_password = "admin"

class TestBase(LiveServerTestCase):
    def create_app(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        # edit the config so that you're not overwriting any important configurations,
        # and making a new local database for testing purposes
        app.config.from_object(Config)
        app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test_app.db'),
        SECRET_KEY="test key",
        WTF_CSRF_ENABLED=False,
        DEBUG=True
        )
        return app
    
    def setUp(self):
        print("<-----NEXT TEST----->")
        chrome_options = Options()
        chrome_options.binary_location = "/usr/bin/chromium-browser"
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=chrome_options)
        self.driver.get("http://localhost:5000")
        db.session.commit()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.driver.quit()
        print("<-----END OF TEST----->")

    def test_server_is_up_and_running(self):
        response = urlopen("http://localhost:5000")
        self.assertEqual(response.code, 200)

class TestHome(TestBase):

    def test_homelink(self):
        self.drive.find_element_by_xpath("/html/body/div[1]/a[1]").click()

        assert url_for("index") in self.driver.current_url

