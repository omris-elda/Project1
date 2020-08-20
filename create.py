from app import db
from app.models import User, Supplier, Stock

db.drop_all()
db.create_all()
