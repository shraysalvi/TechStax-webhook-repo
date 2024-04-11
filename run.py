from app import app
from app.webhook.routes import webhook
app.register_blueprint(webhook)


if __name__ == "__main__":
    app.run(debug=True)

# X-Github-Event: push
# X-Github-Event: pull_request
