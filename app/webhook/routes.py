from flask import Blueprint, json, request

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/receiver', methods=["POST", "GET"])
def receiver():
  if request.is_json:
    print(request.data)
    print(request.headers)
    data = request.get_json()
    # print(data)
    # with open("merge.json", "w") as file:
    #   json.dump(data, file)
    return data, 200
  with open("push.json", "r") as file:
    return json.load(file), 200


# X-Github-Event: push
# X-Github-Event: pull_request
