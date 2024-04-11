from flask import Blueprint, json, request

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/receiver', methods=["POST", "GET"])
def receiver():
  if request.is_json:
    if request.headers['X-Github-Event'] == "push":
      data = request.get_json()
    if request.headers['X-Github-Event'] == "pull_request":
      data = request.get_json()
    return "data", 200


# X-Github-Event: push
# X-Github-Event: pull_request
