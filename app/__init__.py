from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config) # this imports the configuration options from the config.py file
db = SQLAlchemy(app) # sets the database variable
migrate = Migrate(app, db) # this is for updating the database if we need to change the schema
login = LoginManager(app) # this manages logins
login.login_view = "login"
from app import routes, models, errors