from app import app, latest_5_record
from app.webhook.routes import webhook
from flask import render_template
from flask import jsonify
app.register_blueprint(webhook)
from bson.json_util import dumps


@app.route('/')
def index():
    return render_template('index.html', data=latest_5_record())


@app.route('/every-15-seconds')
def every_15_sec():
    return jsonify([dumps(_) for _ in latest_5_record()])


if __name__ == "__main__":
    app.run(debug=True)

# X-Github-Event: push
# X-Github-Event: pull_request
