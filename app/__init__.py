from flask import Flask
from pymongo import MongoClient
import certifi
from flask_bcrypt import Bcrypt

client = MongoClient('', tlsCAFile=certifi.where())
mongo = client['ShareX']


app = Flask(__name__)
app.config.from_object('config')

bcrypt = Bcrypt(app)


