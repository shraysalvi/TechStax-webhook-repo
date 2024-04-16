from flask import Flask
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "`mongodb://mongodb:27017/techstax`")
mongo = PyMongo(app)

DB = mongo.db

def gets():
    try:
        data = DB.githooks.find({})
        return data
    except Exception as e:
        return {"error": str(e)}


def get(_id):
    try:
        data = DB.githooks.find_one({"_id": _id})
        if data:
            return data
        else:
            return {"error": "Event not found"}
    except Exception as e:
        return {"error": str(e)}


def insert(event_data):
    try:
        inserted_id = DB.githooks.insert_one(event_data).inserted_id
        return str(inserted_id)
    except Exception as e:
        return {"error": str(e)}


def update(_id, event_data):
    try:
        result = DB.githooks.update_one({"_id": _id}, {"$set": event_data})
        if result.modified_count > 0:
            return {"message": "Event updated successfully"}
        else:
            return {"error": "Event not found or no changes made"}
    except Exception as e:
        return {"error": str(e)}


def delete(_id):
    try:
        result = DB.githooks.delete_one({"_id": _id})
        if result.deleted_count > 0:
            return {"message": "Event deleted successfully"}
        else:
            return {"error": "Event not found"}
    except Exception as e:
        return {"error": str(e)}

def latest_5_record():
    return DB.githooks.find().sort([("_id", -1)]).limit(5)
