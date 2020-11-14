from flask import Flask, jsonify, request
from sfi.config import ConfigBase
from sfi.logger import logger
from sfi.shoper_client import ShoperWebhookOrderCreate
from sfi.shoper_service import ShoperWebhookCreateOrderService
from sfi.shoper_client import ShoperApiClient
from sfi.fakturownia_client import FakturowniaWebhookProductUpdate
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
        webhooks["shoper"] = shoper_wh_order_create.dict()
        response = ShoperWebhookCreateOrderService(shoper_wh_order_create).handle_request()
        return jsonify({"ok": "ok"})

    @app.route("/api/webhook/fakturownia/product_update", methods=["POST"])
    def webhook_fakturownia_warehouse():
        prod_update = FakturowniaWebhookProductUpdate(**request.json)
        sac = ShoperApiClient()
        quantity = int(prod_update.product.stock_level)
        prod_code = prod_update.product.code
        response = sac.update_product_stock(prod_code=prod_code, quantity=quantity)
        webhooks["fakturownia"] = str(response.text)
        return "{'ok':'ok'}"


    @app.route("/api/fakturownia/request")
    def show_fakturownia_request():
        return jsonify(webhooks["fakturownia"])

    @app.route("/api/shoper/request")
    def show_shoper_request():
        return jsonify(webhooks["shoper"])

    return app
