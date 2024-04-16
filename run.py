from app import app, latest_5_record
from app.webhook.routes import webhook
from flask import render_template
from bson.json_util import dumps
import json
from datetime import datetime


app.register_blueprint(webhook)

@app.template_filter('format_timestamp')
def format_timestamp(timestamp):
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%dth %B %Y - %I:%M %p UTC")


@app.route('/')
def index():
    return render_template('index.html', data=latest_5_record())


@app.route('/every-15-seconds')
def every_15_sec():
    return json.loads(dumps(latest_5_record()))


if __name__ == "__main__":
    app.run()

# X-Github-Event: push
# X-Github-Event: pull_request
