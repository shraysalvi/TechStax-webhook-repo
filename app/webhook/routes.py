from app import insert
from flask import Blueprint, request
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')
from datetime import datetime, timezone 


def merge(data):
    insert({
        "request_id": data.get("after"),
        "author": data.get("commits")[0].get("author").get("username"),
        "action": "merge",
        "from_branch": data.get("before"),
        "to_branch": data.get("after"),
        "timestamp": data.get("head_commit").get("timestamp")
    })


def push(data):
    insert({
        "request_id": data.get("after"),
        "author": data.get("head_commit").get("author").get("username"),
        "action": "push",
        "from_branch": data.get("before"),
        "to_branch": data.get("after"),
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


@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.is_json:
        if request.headers['X-Github-Event'] == "push":

            data = request.get_json()

            if len(data.get("commits")) > 1:
                merge(data)
            else:
                push(data)

        if request.headers['X-Github-Event'] == "pull_request":
            data = request.get_json()
            pull(data)
        return "data", 200
