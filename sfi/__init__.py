from flask import Flask, render_template, Request, Response, jsonify, request
from sfi import email_sender
from sfi import forms
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SMTP_SERVER") or "very_very_secret_key_to_be_changed_in_production"

    @app.route("/test")
    def test():
        return "<h3> ### mrcn ### heroku ### </h3>"

    TEMP_TEXT_FILE = "./temp.json"
    HEADERS_FILE = "./headers.txt"

    @app.route("/api/webhook", methods=["POST"])
    def webhook_order_change_status():
        headers = request.headers
        body = request.json
        with open(TEMP_TEXT_FILE, "w+") as file:
            file.write(str(body))
        with open(HEADERS_FILE, "w+") as file:
            file.write(str(headers))
        return jsonify({"status": "OK"})

    @app.route("/check_temp", methods=["GET"])
    def check_temp_text_file():
        with open(TEMP_TEXT_FILE, "r") as file:
            resp = file.read()
        return resp

    @app.route("/check_headers", methods=["GET"])
    def check_headers():
        with open(HEADERS_FILE, "r") as file:
            resp = file.read()
        return resp

    return app
