import os
import json
import requests
from pydantic import BaseModel
from typing import List, Optional, Dict


# MODELS
class FakturowniaProduct(BaseModel):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    price_net: Optional[str]
    tax: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    automatic_sales: Optional[bool]
    limited: Optional[bool]
    warehouse_quantity: Optional[str]
    available_from: Optional[str]
    available_to: Optional[str]
    payment_callback: Optional[str]
    payment_url_ok: Optional[str]
    payment_url_error: Optional[str]
    token: Optional[str]
    quantity: Optional[str]
    quantity_unit: Optional[str]
    additional_info: Optional[str]
    disabled: Optional[bool]
    price_gross: Optional[str]
    price_tax: Optional[str]
    form_fields_horizontal: Optional[bool]
    form_fields: Optional[str]
    form_name: Optional[str]
    form_description: Optional[str]
    quantity_sold_outside: Optional[str]
    form_kind: Optional[str]
    form_template: Optional[str]
    elastic_price: Optional[bool]
    next_product_id: Optional[str]
    quantity_sold_in_invoices: Optional[str]
    deleted: Optional[str]
    code: Optional[str]
    currency: Optional[str]
    ecommerce: Optional[bool]
    period: Optional[str]
    show_elastic_price: Optional[bool]
    elastic_price_details: Optional[str]
    elastic_price_date_trigger: Optional[str]
    iid: Optional[str]
    purchase_price_net: Optional[str]
    purchase_price_gross: Optional[str]
    use_formula: Optional[bool]
    formula: Optional[str]
    formula_test_field: Optional[str]
    stock_level: Optional[str]
    sync: Optional[bool]
    category_id: Optional[str]
    kind: Optional[str]
    package: Optional[bool]
    package_product_ids: Optional[str]
    department_id: Optional[str]
    use_product_warehouses: Optional[bool]
    purchase_price_tax: Optional[str]
    purchase_tax: Optional[str]
    service: Optional[bool]
    use_quantity_discount: Optional[bool]
    quantity_discount_details: Optional[str]
    price_net_on_payment: Optional[bool]
    warehouse_numbers_updated_at: Optional[str]
    ean_code: Optional[str]
    weight: Optional[str]
    weight_unit: Optional[str]
    size_height: Optional[str]
    size_width: Optional[str]
    size: Optional[str]
    size_unit: Optional[str]
    auto_payment_department_id: Optional[str]
    attachments_count: Optional[str]
    image_url: Optional[str]
    tax2: Optional[str]
    purchase_tax2: Optional[str]
    supplier_code: Optional[str]
    package_products_details: Optional[str]
    siteor_disabled: Optional[bool]
    use_moss: Optional[bool]
    subscription_id: Optional[str]
    accounting_id: Optional[str]
    status: Optional[str]
    restricted_to_warehouses: Optional[bool]
    gtu_codes: List
    tag_list: List
    electronic_service: Optional[str]


class NewInvoiceRequestBodyNoCustomerTaxId(BaseModel):
    buyer_name: Optional[str]
    buyer_post_code: Optional[str]
    buyer_city: Optional[str]
    buyer_street: Optional[str]
    buyer_first_name: Optional[str]
    buyer_country: Optional[str]
    buyer_email: Optional[str]
    buyer_www: Optional[str]
    buyer_fax: Optional[str]
    buyer_phone: Optional[str]
    buyer_tax_no: Optional[str]
    positions: List[Dict]


class NewInvoiceRequest(BaseModel):
    api_token: str


class NewInvoiceRequestNoTaxId(NewInvoiceRequest):
    invoice: NewInvoiceRequestBodyNoCustomerTaxId


class FakturowniaWebhookProductUpdateProduct(BaseModel):
    category_name: Optional[str]
    code: Optional[str]  # DS025016030,
    currency: Optional[str]
    description: Optional[str]
    disabled: Optional[str]
    external_ids: Optional[Dict]
    name: Optional[str]
    price_gross: Optional[str]
    price_net: Optional[str]
    skip_webhooks: Optional[str]
    stock_level: Optional[str]
    tax: Optional[str]


class FakturowniaWebhookProductUpdate(BaseModel):  # ShoperWebhookOrderCreate
    api_token: Optional[str]
    app_name: Optional[str]
    locale: Optional[str]
    product: FakturowniaWebhookProductUpdateProduct
    ...


class FakturowniaApiClient:

    def __init__(self, fakturownia_base_url: str = None, fakturownia_token: str = None):
        self.token = fakturownia_token or os.getenv("FAKTUROWNIA_API_TOKEN")
        self.fakturowania_base_url = fakturownia_base_url or os.getenv("FAKTUROWNIA_BASE_URL")

    def yield_products(self):
        page = 1
        with requests.Session() as session:
            while True:
                response = session.get(f"{self.fakturowania_base_url}/products.json?api_token={self.token}&page={page}")
                for prod in response.json():
                    yield FakturowniaProduct(**prod)
                page = page + 1
                if not response.json():
                    break

    def get_prod_by_id(self, id) -> dict:
        url = f"{self.fakturowania_base_url}/products/{id}.json?api_token={self.token}"
        resp = requests.get(url)
        return resp.json()

    def create_new_invoice(self, new_invoice: NewInvoiceRequest):
        url = f"{self.fakturowania_base_url}/invoices.json"
        raw_data = json.dumps(new_invoice.dict())
        resp = requests.post(url=url, data=raw_data,
                             headers={'Accept': 'application/json', 'Content-Type': 'application/json'})
