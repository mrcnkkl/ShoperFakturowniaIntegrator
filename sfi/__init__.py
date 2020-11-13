from flask import Flask, jsonify, request
from sfi.config import ConfigBase
from sfi.logger import logger
from sfi.shoper_client import ShoperWebhookOrderCreate
from sfi.shoper_service import ShoperWebhookCreateOrderService
import random

webhooks = {
    "fakturownia": "",
    "shoper": ""
}


def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigBase)

    @app.route("/api/health", methods=["GET"])
    @app.route("/", methods=["GET"])
    def health():
        logger().info(f"Checking health from: {request.remote_addr}")
        return jsonify({"status": f"OK: {random.random()}"})

    @app.route("/api/webhook/shoper/order_create", methods=["POST"])
    def webhook_shoper_create_order():
        shoper_wh_order_create = ShoperWebhookOrderCreate(**request.json)
        response = ShoperWebhookCreateOrderService(shoper_wh_order_create).handle_request()
        return jsonify({"ok": "ok"})

    @app.route("/api/webhook/fakturownia/warehouse", methods=["POST"])
    def webhook_fakturownia_warehouse():
        req = request.json
        webhooks["fakturownia"] = dict(req)
        return "{'ok':'ok'}"

    @app.route("/api/fakturownia/request")
    def show_fakturownia_request():
        return jsonify(webhooks["fakturownia"])

    return app
