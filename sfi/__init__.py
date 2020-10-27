from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route("/test")
    def test():
        return "<h3> ### mrcn ### heroku ### </h3>"

    return app
