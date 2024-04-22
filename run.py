from app import app
from app.extensions import last_15min
from app.webhook.routes import webhook
from flask import render_template
from bson.json_util import dumps
import json


app.register_blueprint(webhook)


@app.template_filter('format_utc_timestamp')
def format_utc_timestamp(timestamp):
    """
    Formats a given timestamp string into a specific format.

    Args:
        timestamp (datetime): The timestamp in Zulu UTC format.

    Returns:
        str: The formatted timestamp string in the format "ddth Month Year - HH:MM AM/PM UTC".
    """
    return timestamp.strftime("%dth %B %Y - %I:%M %p UTC")


@app.route('/')
def index():
    return render_template('index.html', data=last_15min())


@app.route('/every-15-seconds')
def every_15_sec():
    return json.loads(dumps(last_15min()))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
