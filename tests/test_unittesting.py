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
            first_name="admin", 
            last_name="admin",
            email = "admin@admin.com",
            password = hashed_pw1
        )
        # creating the second test user
        hashed_pw_2 = generate_password_hash("password")
        testuser = User(
            username = "test",
            email = "test@user.com",
            password = hashed_pw_2
        )
        # creating a test supplier
        testsupplier = Supplier(
            supplier_name = "TestSupplier",
            supplier_description = "Test Supplier Description"
        )
        # creating a test product, linked to the test supplier
        testproduct = Stock(
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
