from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

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


class Supplier(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    supplier_name = db.Column(db.String(100), index = True)
    supplier_description = db.Column(db.String(500))
    stock = db.relationship("Stock", backref="supplier", lazy="dynamic")

    def __repr__(self):
        return "<Supplier: {}>\n\r".format(self.supplier_name), "<Supplier Description: {}\n\r".format(self.supplier_description)


class Stock(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(50), index = True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("supplier.id"))
    product_price = db.Column(db.String(5))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        output = "<Product: {}\n\r".format(self.product_name),
        "<Supplier: {}\n\r".format(self.supplier_id),
        "<Price: {}\n\r".format(self.product_price)
        return output