from app import insert
from flask import Blueprint, request
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')
from datetime import datetime, timezone 
import json


def merge(data):
    insert({
        "request_id": data.get("after"),
        "author": data.get("commits")[1].get("author").get("username"),
        "action": "merge",
        "from_branch": data.get("commits")[0].get("url"),
        "to_branch": data.get("commits")[1].get("url"),
        "timestamp": data.get("head_commit").get("timestamp")
    })


def pull(data):
    insert({
        "request_id": data.get("pull_request").get("head").get("sha"),
        "author": data.get("pull_request").get("head").get("repo").get("owner").get("login"),
        "action": "pull_request",
        "from_branch": data.get("pull_request").get("head").get("repo").get("full_name"),
        "to_branch": data.get("repository").get("full_name"),
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat()
    })


def push(data):
    repo = data.get("repository").get("full_name")
    insert({
        "request_id": data.get("after"),
        "author": data.get("head_commit").get("author").get("username"),
        "action": "push",
        "from_branch": repo,
        "to_branch": repo,
        "timestamp": data.get("head_commit").get("timestamp")
    })


@webhook.route('/receiver', methods=["POST", "GET"])
def receiver():
    if request.is_json:
        if request.headers['X-Github-Event'] == "push":

            data = request.get_json()

            # with open("merge.json", "w") as file:
            #     json.dump(data, file)

            if len(data.get("commits")) > 1:
                merge(data)
            else:
                push(data)

        if request.headers['X-Github-Event'] == "pull_request":
            data = request.get_json()
            pull(data)
        return "", 200