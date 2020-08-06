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
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

# setting the test variables for test admin user
test_admin_username =  "admin"
test_admin_email = "admin@admin.com"
test_admin_password = "admin"
test_new_username = "newuser"
test_new_email = "newtest@newtest.com"
test_new_password = "newpassword"

class TestBase(LiveServerTestCase):
    def create_app(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        # edit the config so that you're not overwriting any important configurations,
        # and making a new local database for testing purposes
        app.config.from_object(Config)
        app.config.update(SQLALCHEMY_DATABASE_URI=os.environ.get("TEST_DATABASE_URI"),
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
        self.driver = webdriver.Chrome(executable_path="/home/edmundtheeel/chromedriver", chrome_options=chrome_options)
        self.driver.get("http://localhost:5000")

        db.session.commit()
        db.drop_all()
        db.create_all()

        # creating the first test user
        hashed_pw1 = generate_password_hash("admin")
        admin = User(
            username = "admin",
            email = "admin@admin.com",
            password_hash = hashed_pw1
        )
        # creating the second test user
        hashed_pw_2 = generate_password_hash("password")
        testuser = User(
            username = "test",
            email = "test@user.com",
            password_hash = hashed_pw_2
        )
        # creating a test supplier
        testsupplier = Supplier(
            supplier_id = 1,
            supplier_name = "TestSupplier",
            supplier_description = "Test Supplier Description"
        )
        # creating a test product, linked to the test supplier
        testproduct = Stock(
            product_id = 1,
            product_name = "Test Product",
            product_price = 100.50,
            current_stock = 5,
            supplier_id = 1
        )
        # adds the test data to the database
        db.session.add(admin)
        db.session.add(testuser)
        db.session.add(testsupplier)
        db.session.add(testproduct)
        db.session.commit()

    def tearDown(self):
        self.driver.quit()
        print("<-----END OF TEST----->")

    # def test_server_is_up_and_running(self):
    #     response = urlopen("http://localhost:5000")
    #     self.assertEqual(response.code, 200)

class TestNavBar(TestBase):

    def test_homelink(self):
        self.driver.find_element_by_xpath("/html/body/div[1]/a[1]").click()

        assert url_for("index") in self.driver.current_url

    def test_registerlink(self):
        self.driver.find_element_by_xpath("/html/body/div/a[3]").click()

        assert url_for("register") in self.driver.current_url
    
    def test_loginlink(self):
        self.driver.find_element_by_xpath("/html/body/div[1]/a[2]").click()

        assert url_for("login") in self.driver.current_url

class TestInput(TestBase):

    def test_login(self):

        self.driver.find_element_by_xpath("/html/body/div[1]/a[2]").click()
        time.sleep(1)
        assert url_for("login") in self.driver.current_url
        # inputs the test admin username
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(test_admin_username)
        # inputs the test admin password
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(test_admin_password)
        # click the sign in button
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        # checks that you've logged in correctly
        assert url_for("index") in self.driver.current_url

    def test_register(self):

        self.driver.find_element_by_xpath("/html/body/div/a[3]").click()
        time.sleep(1)
        assert url_for("register") in self.driver.current_url
        # input the new test user
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(test_new_username)
        # input the test user email
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(test_new_email)
        # input the test user password x2
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(test_new_password)
        self.driver.find_element_by_xpath('//*[@id="password2"]').send_keys(test_new_password)
        # click the register button
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(1)
        # checks that you've made an account and been redirected to the login page
        assert url_for("login") in self.driver.current_url

