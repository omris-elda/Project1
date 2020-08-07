import unittest
from os import getenv
import os
from flask import url_for
from app import app, db
from app.models import Stock, Supplier, User
from config import Config
from flask_testing import TestCase
from werkzeug.security import generate_password_hash, check_password_hash
from tests.test_views import TestBase

class TestSupplierInput(TestBase):
    # the tests for inputting on supplier pages
    def test_newsupplier(self):
        with self.client:
            self.client.post(
                url_for("login"),
                data = dict(
                    username = "test",
                    password = "password"
                ),
                follow_redirects = True
            )
            response = self.client.post(
                url_for("add_supplier"),
                data = dict(
                    supplier_name = "New Test Supplier",
                    supplier_description = "New Test Supplier Description"
                ),
                follow_redirects = True
            )
            self.assertIn(b"Add Supplier", response.data),
            self.assertEqual(response.status_code, 200)

    def test_editsupplier(self):
        with self.client:
            self.client.post(
                url_for("login"),
                data = dict(
                    username = "test",
                    password = "password"
                ),
                follow_redirects = True
            )
            response = self.client.post(
                url_for("edit_supplier", supplier_id = 1),
                data = dict(
                    supplier_name = "Updated Test Supplier",
                    supplier_description = "Updated Test Supplier Description"
                ),
                follow_redirects = True
            )
            self.assertIn(b"Updated Test Supplier", response.data),
            self.assertEqual(response.status_code, 200)

class TestProductInput(TestBase):
    # the tests for inputting on product pages
    def test_addproduct(self):
        with self.client:
            self.client.post(
                url_for("login"),
                data = dict(
                    username = "test",
                    password = "password"
                ),
                follow_redirects = True
            )
            response = self.client.post(
                url_for("add_stock"),
                data = dict(
                    product_name = "New Product",
                    product_price = 19.50,
                    supplier_id = 1,
                    current_stock = 5
                ),
                follow_redirects = True
            )
            self.assertIn(b"Add Stock", response.data),
            self.assertEqual(response.status_code, 200)

    def test_editproduct(self):
        with self.client:
            self.client.post(
                url_for("login"),
                data = dict(
                    username = "test",
                    password = "password"
                ),
                follow_redirects = True
            )
            response = self.client.post(
                url_for("edit_product", product_id = 1),
                data = dict(
                    supplier_name = "Updated Test Supplier",
                    supplier_description = "Updated Test Supplier Description"
                ),
                follow_redirects = True
            )
            self.assertIn(b"Updated Test Supplier", response.data),
            self.assertEqual(response.status_code, 200)

class TestUserInput(TestBase):
    # the tests for inputting on user pages
    def test_register(self):
        with self.client:
            response = self.client.post(
                url_for('register'),
                data = dict(
                    email = "new@user.com",
                    password = "password",
                    confrim_password = "password",
                    username = "NewTestUser"
                ),
                follow_redirects = True
            )
            self.assertIn(b"Login", response.data)
            self.assertEqual(response.status_code, 200)

    def test_logout(self):
        with self.client:
            response = self.client.get(
                '/logout',
                follow_redirects = True
            )
            self.assertIn(b"Sign In", response.data)
            self.assertEqual(response.status_code, 200)

    def test_login(self):
        with self.client:
            response = self.client.post(
                url_for('login'),
                data = dict(
                    username = "test",
                    password = "password"
                ),
                follow_redirects = True
            )
            self.assertIn(b"Home", response.data)
            self.assertEqual(response.status_code, 200)

    def test_edit_account(self):
        with self.client:
            response = self.client.post(
                url_for('login'),
                data = dict(
                    username = "test",
                    password = "password"
                ),
                follow_redirects = True
            )
            self.assertIn(b"Home", response.data)
            self.assertEqual(response.status_code, 200)
            response = self.client.post(
                url_for("edit_profile"),
                data = dict(
                    username = "updated test",
                    email = "updated@test.com",
                ),
                follow_redirects = True
            )
            self.assertIn(b"Your changes have been saved", response.data)
            self.assertEqual(response.status_code, 200)

    def test_add_stock(self):
        with self.client:
            response = self.client.post(
                url_for('login'),
                data = dict(
                    username = "test",
                    password = "password"
                ),
                follow_redirects = True
            )
            self.assertIn(b"Home", response.data)
            self.assertEqual(response.status_code, 200)
            response = self.client.post(
                data = dict(
                    product_name = "New Product",
                    product_price = "1.50",
                    supplier = "TestSupplier",
                    current_stock = "100"
                ),
                follow_redirects = True
            )
            self.assertIn(b"Stock has been added", response.data)
            self.assertEqual(response.status_code, 200)
"""tests for later if I get time:
add stock
edit product
delete supplier
delete product
"""