from os.path import abspath, join, dirname
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = abspath(join(dirname(__file__), 'database'))

application = Flask(__name__)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + BASE_DIR +'/database.db'
db = SQLAlchemy(application)
