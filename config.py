import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") # or \
        # 'sqlite:///' + os.path.join(basedir, 'app.db') # or see startup instructions in flask blog
        # the above code has generated a temporary SQLite db for testing purposes.

    SQLALCHEMY_TRACK_MODIFICATIONS = False