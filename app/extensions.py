from flask_pymongo import PyMongo

# Setup MongoDB here
mongo = PyMongo(uri="mongodb://localhost:27017/techstax")
collection = mongo.db.events

