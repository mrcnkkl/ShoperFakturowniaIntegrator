from flask import Flask, render_template, Request, Response, jsonify, request
from sfi import email_sender
from sfi import forms
import os
import hashlib
from sfi.shoper_client import ShoperWebhookOrderCreate
import logging
from pprint import pformat

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger("## sfi ##")


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SMTP_SERVER") or "very_very_secret_key_to_be_changed_in_production"

    @app.route("/test", methods=["GET", "POST"])
    def test():
        body = request.json
        logger.info(type(body))
        data = request.data
        print(data)
        return "<h3> ### mrcn ### heroku ### </h3>"

    TEMP_TEXT_FILE = "./temp.json"
    HEADERS_FILE = "./headers.txt"
    SHA_FILE = "./sha.txt"

    def _calculate_webhook_sha(webhook_id, user_secret, webhook_data):
        load = str.encode(webhook_id) + b":" + str.encode(user_secret) + b":" + str.encode(webhook_data)
        return hashlib.sha1(load).hexdigest()

    @app.route("/api/webhook", methods=["POST"])
    def webhook_order_change_status():
        headers = request.headers
        body = request.json
        with open(TEMP_TEXT_FILE, "w+") as file:
            file.write(str(body))
        with open(HEADERS_FILE, "a+") as file:
            file.write(str(headers))
        with open(SHA_FILE, "w+") as file:
            file.write(_calculate_webhook_sha("3", "21497ED1A0D3B473004E2A061A12AD2AF28BAAC2E6B3B7CE046C0E17340A3F47",
                                              request.data.decode("utf-8")))
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

    @app.route("/check_sha", methods=["GET"])
    def check_sha():
        with open(SHA_FILE, "r") as file:
            resp = file.read()
        return resp

    @app.route("/api/webhook/order_create", methods=["POST"])
    def webhook_order_create():
        headers = request.headers
        body = request.json
        shoper_wh_order_create = ShoperWebhookOrderCreate(**body)

        logger.info(shoper_wh_order_create.dict())

        print(f"\n")
        print(f"\n")
        print(f"\n")
        data = request.data
        print(data)
        print(f"\n")
        print(f"\n")
        print(f"\n")

        with open(TEMP_TEXT_FILE, "w+") as file:
            file.write(pformat(shoper_wh_order_create.dict()))
        with open(HEADERS_FILE, "a+") as file:
            file.write(str(headers))
        with open(SHA_FILE, "w+") as file:
            file.write(_calculate_webhook_sha("4", "21497ED1A0D3B473004E2A061A12AD2AF28BAAC2E6B3B7CE046C0E17340A3F47",
                                              request.data.decode("utf-8")))
        return jsonify({"status": "OK"})

    # /api/webhook/fakturownia/product_update
    @app.route("/api/webhook/order_create", methods=["POST"])
    def webhook_fakturownia_product_update():
        headers = request.headers
        body = request.json

        print(f"\n")
        print(f"\n")
        print(f"\n")
        data = request.data
        print(data)
        print(f"\n")
        print(f"\n")
        print(body)
        print(f"\n")
        print(f"\n")

        return jsonify({"status": "OK"})

    return app
