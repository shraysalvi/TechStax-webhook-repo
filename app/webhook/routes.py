from datetime import datetime, timezone
from app.extensions import insert
from flask import Blueprint, request
import json
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


def ist_iso_to_zulu_utc(datetime_str):
    """
    Convert a datetime string in IST (Indian Standard Time) to Zulu time (UTC).

    Args:
        datetime_str (str): The datetime string in the format "%Y-%m-%dT%H:%M:%S%z".

    Returns:
        str: The converted datetime string in Zulu time (UTC) format "%Y-%m-%dT%H:%M:%SZ".
    """
    dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
    output_str = dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return output_str


def merge(data: dict):
    """
    This function is responsible for storing the data in the database when a merge event is triggered.

    Args:
        data (dict): Dictionary containing the data from the webhook.
    """
    try:
        return insert({
            "request_id": data["pull_request"]["id"],
            "author": data["pull_request"]["merged_by"]["login"],
            "action": "merge",
            "from_branch": data["pull_request"]["head"]["repo"]["full_name"],
            "to_branch": data["pull_request"]["base"]["repo"]["full_name"],
            "timestamp": datetime.strptime(data["pull_request"]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        }), 200
    except Exception as e:
        return {"error": str(e)}, 400


def pull(data: dict):
    """
    This function is responsible for storing the data in the database when a pull request event is triggered.

    Args:
        data (dict): Dictionary containing the data from the webhook.
    """
    try:
        return insert({
            "request_id": data["pull_request"]["id"],
            "author": data["pull_request"]["user"]["login"],
            "action": "pull_request",
            "from_branch": data["pull_request"]["head"]["repo"]["full_name"],
            "to_branch": data["repository"]["full_name"],
            "timestamp": datetime.strptime(data["pull_request"]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        }), 200
    except Exception as e:
        return {"error": str(e)}, 400


def push(data: dict):
    """
    This function is responsible for storing the data in the database when a push event is triggered.

    Args:
        data (dict): Dictionary containing the data from the webhook.
    """

    try:
        return insert({
            "request_id": data["after"],
            "author": data["commits"][-1]["author"]["username"],
            "action": "push",
            "to_branch": data["repository"]["full_name"],
            "timestamp": datetime.strptime(ist_iso_to_zulu_utc(data["commits"][-1]["timestamp"]), "%Y-%m-%dT%H:%M:%SZ")
        }), 200
    except Exception as e:
        return {"error": str(e)}, 400


@webhook.route('/receiver', methods=["POST"])
def receiver():
    """
    This function is responsible for receiving the webhook from github and storing the data in the database.
    """
    if request.is_json:
        if request.headers.get('X-Github-Event', None) == "push":
            data = request.get_json()

            # with open("push-merge.json", "w") as file:
            #     json.dump(data, file)

            return push(data)

        elif request.headers.get('X-Github-Event', None) == "pull_request":
            data = request.get_json()

            # with open("pull-merge.json", "w") as file:
            #     json.dump(data, file)

            if data["pull_request"]["merged"]:
                return merge(data)
            else:
                return pull(data)
        else:
            return {"error": "Unsupported Event"}, 400
    else:
        return {"error": "Expected Json Data"}, 400

# TODO:
# explain the code - https://www.tornadoweb.org/en/stable/guide/queues.html
# multithreading vs multiprocessing
