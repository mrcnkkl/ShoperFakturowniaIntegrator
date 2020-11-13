import sfi
import pytest
from requests import Response
from tests import resources
from sfi.shoper_client import ShoperWebhookOrderCreate
from sfi.shoper_service import ShoperWebhookCreateOrderService


@pytest.fixture
def client():
    app = sfi.create_app()
    yield app.test_client()


@pytest.fixture
def webhook_create_order_body():
    yield resources.webhook_create_order_body


@pytest.fixture
def shoper_webhook_order():
    yield ShoperWebhookOrderCreate(**resources.webhook_create_order_body)


@pytest.fixture()
def fakturownia_clients_by_id_response():
    yield resources.fakturownia_customers_by_id


def test_health_returns_200(client):
    resp: Response = client.get('/api/health')
    assert resp.status_code == 200


def test_ShoperWebhookCreateOrderService_get_product_positions(shoper_webhook_order):
    swcoservice = ShoperWebhookCreateOrderService(shoper_webhook_order, object(), object())
    print(swcoservice.get_product_positions())


# new_invoice_call_body_no_cust_tax_id
def test_ShoperWebhookCreateOrderService_new_invoice_call_body_no_cust_tax_id(shoper_webhook_order):
    swcoservice = ShoperWebhookCreateOrderService(shoper_webhook_order, object(), object())
    print(swcoservice.new_invoice_call_body().dict())
