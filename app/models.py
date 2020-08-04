from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

"""
This is the user table model, which defines the table within the database.
Some of the fields have restraints on them, such as the unique, which means
that every entry has to be unique and cannot be duplicated within the database,
as well as the index restraint which allows them to be searched a bit more easily.
While that's not very important for such a small application, for bigger apps 
it can speed up search functions significantly.
"""
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

"""
This is the supplier model to create the supplier table in the database. Similar to the above
model, the only real difference is that there's a relationship here between the supplier and
the stock table (which is below), which will allow for cross-referencing with ease.
"""
class Supplier(db.Model):

    supplier_id = db.Column(db.Integer, primary_key = True)
    supplier_name = db.Column(db.String(100), index = True, unique = True)
    supplier_description = db.Column(db.String(500))
    stock = db.relationship("Stock", backref="supplier", lazy="dynamic")

    def __repr__(self):
        return "<Supplier: {}>\n\r".format(self.supplier_name), "<Supplier Description: {}\n\r".format(self.supplier_description)

"""
This is the stock model which is used to create the stock table in the database.
Again, this is similar to the previous models, with the foreign key from the supplier
table allowing for easy cross-referencing.
"""
class Stock(db.Model):

    product_id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(50), index = True, unique = True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("supplier.supplier_id"))
    product_price = db.Column(db.String(5))
    current_stock = db.Column(db.Integer)
    def __repr__(self):
        output = "<Product: {}\n\r".format(self.product_name),
        "<Supplier: {}\n\r".format(self.supplier_id),
        "<Price: {}\n\r".format(self.product_price)
        return output

"""
Thanks to the flask-migrate extension, these database schemas can be quite
easily updated through the console. To update them, all you have to do is
update them in this file, ensure that flask-migrate is installed, and then run
flask db init (to initialise the migration process/make the database if it doesn't already exist)
flask db migrate (to migrate any changes)
flask db upgrade (to apply any changes made in the migration folder)
You can also roll these changes back should they break anything, using
flask db downgrade
which undoes the previous migration.
"""