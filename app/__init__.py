from flask import Flask
from flask_pymongo import PyMongo
import os
from logging import config


# application and db config
app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/techstax")
mongo = PyMongo(app)


# log configs
config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "prod": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "./logs/record.log",
                "maxBytes": 1000000,
                "backupCount": 5,
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["console", "prod"]},
    }
)

