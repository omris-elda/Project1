import unittest
from os import getenv
import os
from flask import url_for

from app import app, db
from app.models import Stock, Supplier, User
from config import Config
from flask_testing import TestCase
from werkzeug.security import generate_password_hash, check_password_hash

class TestBase(TestCase):

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
        # start by recreating the database from scratch
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
        # destroys the database so that it has to be rebuilt for every test, 
        # ensuring that there's no cross-contamination from one test to another
        db.session.remove()
        db.drop_all()

class TestViews(TestBase):
    # testing to make sure that all the pages load correctly when you're not logged out
    def test_notloggedin_pages(self):
        response = self.client.get(url_for("index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello", response.data)
        response = self.client.get(url_for("register"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)
        response = self.client.get(url_for("logout"), follow_redirects = True)
        self.assertEqual(response.status_code, 301)
        response1 = self.client.get(url_for("login"), follow_redirects = True)
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.get(url_for("user", username = "test"), follow_redirects = True)
        self.assertEqual(response2.status_code, 301)
        response3 = self.client.get(url_for("edit_profile"), follow_redirects = True)
        self.assertEqual(response3.status_code, 301)
        response4 = self.client.get(url_for("add_stock"), follow_redirects = True)
        self.assertEqual(response4.status_code, 301)
        response5 = self.client.get(url_for("add_supplier"), follow_redirects = True)
        self.assertEqual(response5.status_code, 301)
        response6 = self.client.get(url_for("edit_supplier", supplier_id = 1), follow_redirects = True)
        self.assertEqual(response6.status_code, 301)
        response7 = self.client.get(url_for("edit_product", product_id = 1), follow_redirects = True)
        self.assertEqual(response7.status_code, 301)
        response8 = self.client.get(url_for("view_product", product_id = 1), follow_redirects = True)
        self.assertEqual(response8.status_code, 301)
        response9 = self.client.get(url_for("view_supplier", supplier_id = 1), follow_redirects = True)
        self.assertEqual(response9.status_code, 301)
        response10 = self.client.get(url_for("delete_supplier", supplier_id = 1), follow_redirects = True)
        self.assertEqual(response10.status_code, 301)
        response11 = self.client.get(url_for("delete_product", product_id = 1), follow_redirects = True)
        self.assertEqual(response11.status_code, 301)

        self.assertIn(b"Sign In", response.data)
        self.assertIn(b"Sign In", response1.data)
        self.assertIn(b"Sign In", response2.data)
        self.assertIn(b"Sign In", response3.data)
        self.assertIn(b"Sign In", response4.data)
        self.assertIn(b"Sign In", response5.data)
        self.assertIn(b"Sign In", response6.data)
        self.assertIn(b"Sign In", response7.data)
        self.assertIn(b"Sign In", response8.data)
        self.assertIn(b"Sign In", response9.data)
        self.assertIn(b"Sign In", response10.data)
        self.assertIn(b"Sign In", response11.data)
    
    def test_users(self):
        with self.client:
            self.client.post(
                url_for("login"),
                data = dict(
                    username = "test",
                    password = "password"
                ),
                follow_redirects = True
            )
            response = self.client.get(url_for("edit_profile"))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Edit Profile", response.data)
            response = self.client.get(url_for("user", username = "test"))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"User: ", response.data)
            response = self.client.get(url_for("logout"), follow_redirects = True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Hello", response.data)
    
    def test_stock_pages(self):
        with self.client:
            self.client.post(
                url_for("login"),
                data = dict(
                    username = "test",
                    password = "password"
                ),
                follow_redirects = True
            )
            response = self.client.get(url_for("add_stock"))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Add Stock", response.data)
            response = self.client.get(url_for("edit_product", product_id = 1))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Edit Stock", response.data)
            response = self.client.get(url_for("view_product", product_id = 1))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Details for ", response.data)

    def test_supplier_pages(self):
        with self.client:
            self.client.post(
                url_for("login"),
                data = dict(
                    username = "test",
                    password = "password"
                ),
                follow_redirects = True
            )
            response = self.client.get(url_for("add_supplier"))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Add Supplier", response.data)
            response = self.client.get(url_for("edit_supplier", supplier_id = 1))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Edit Supplier", response.data)
            response = self.client.get(url_for("view_supplier", supplier_id = 1))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Details for ", response.data)
