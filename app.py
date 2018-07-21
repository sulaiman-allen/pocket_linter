from os.path import abspath, join, dirname
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = abspath(join(dirname(__file__), 'database'))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + BASE_DIR +'/database.db'
db = SQLAlchemy(app)
