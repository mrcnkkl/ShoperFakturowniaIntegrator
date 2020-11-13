import os
import requests
from time import sleep
from pydantic import BaseModel
from typing import List, Optional
from sfi import codes
from sfi import fakturownia_client
from time import sleep


class ShoperApiClient:

    def __init__(self, shoper_user: str = None, shoper_password: str = None, shoper_base_url: str = None,
                 token: str = None):
        self.shoper_user = shoper_user or os.getenv("SHOPER_USER") or "api_admin"
        self.shoper_password = shoper_password or os.getenv("SHOPER_PASSWD")
        self.shoper_base_url = shoper_base_url or os.getenv("SHOPER_BASE_URL")
        self.token = token or os.getenv("SHOPER_TOKEN") or self._get_token()
        print(f"Shoper token = {self.token}")
        self.auth_header = {"Authorization": f"Bearer {self.token}"}

    def _get_token(self):
        URL = f"{self.shoper_base_url}/auth"
        resp = requests.post(URL, auth=requests.auth.HTTPBasicAuth(self.shoper_user, self.shoper_password)).json()
        token = resp['access_token']
        return token

    def get_order_by_id(self, id: str):
        resp: requests.Response = requests.get(f"{self.shoper_base_url}/orders/{id}", headers=self.auth_header)
        return resp

    def get_order_products_filtered_by_order_id(self, order_id: int):
        URL = f"{self.shoper_base_url}/order-products?filters={{\"order_id\": \"{order_id}\" }}"
        response: requests.Response = requests.get(URL, headers=self.auth_header)
        return response

    def get_product_by_id(self, id):
        URL = f"{self.shoper_base_url}/products/{id}"
        response: requests.Response = requests.get(URL, headers=self.auth_header)
        return response

    def get_products(self):
        print(f"get_products called")
        headers = {"Authorization": f"Bearer {self.token}"}
        print(headers)
        page, pages = 1, 1

        with requests.Session() as session:
            while True:
                sleep(1)
                URL = f"{self.shoper_base_url}/products?page={page}"
                response = session.get(URL, headers=headers)
                pages = response.json()["pages"]
                page = response.json()["page"] + 1
                for product in response.json()["list"]:
                    yield product
                if page >= pages:
                    break


### MODELS ###
class ShoperOrderAddress(BaseModel):
    address_id: Optional[str]
    order_id: Optional[str]
    type: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    company: Optional[str]
    tax_id: Optional[str]
    pesel: Optional[str]
    city: Optional[str]
    postcode: Optional[str]
    street1: Optional[str]
    street2: Optional[str]
    state: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    country_code: Optional[str]


class ShoperBillingAddress(ShoperOrderAddress):
    ...


class ShoperOrderShipping(BaseModel):
    shipping_id: Optional[str]
    cost: Optional[str]
    depend_on_w: Optional[str]
    tax_id: Optional[str]
    max_weight: Optional[str]
    min_weight: Optional[str]
    free_shipping: Optional[str]
    order: Optional[str]
    pkwiu: Optional[str]
    mobile: Optional[str]
    engine: Optional[str]
    zone_id: Optional[str]
    callback_url: Optional[str]
    warehouse_id: Optional[str]
    translation_id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    is_default: Optional[str]


class ShoperOrderStatus(BaseModel):
    status_id: Optional[str]
    default: Optional[str]
    color: Optional[str]
    type: Optional[str]
    email_change: Optional[str]
    order: Optional[str]
    name: Optional[str]
    message: Optional[str]


class ShoperOrderPayment(BaseModel):
    payment_id: Optional[str]
    name: Optional[str]
    order: Optional[str]
    title: Optional[str]
    description: Optional[str]
    notify_mail: Optional[str]


class ShoperOrderProduct(BaseModel):
    id: Optional[str]
    order_id: Optional[str]
    product_id: Optional[str]
    stock_id: Optional[str]
    price: Optional[str]
    discount_perc: Optional[str]
    quantity: Optional[str]
    delivery_time: Optional[str]
    name: Optional[str]
    code: Optional[str]
    pkwiu: Optional[str]
    tax: Optional[str]
    tax_value: Optional[str]
    unit: Optional[str]
    option: Optional[str]
    unit_fp: Optional[str]
    weight: Optional[str]
    type: Optional[str]
    loyalty: Optional[str]
    delivery_time_hours: Optional[str]
    text_options: Optional[List]
    file_options: Optional[List]


class ShoperOrderAdditionalField(BaseModel):
    field_id: Optional[str]
    type: Optional[str]
    locate: Optional[str]
    req: Optional[str]
    active: Optional[str]
    order: Optional[str]
    value: Optional[str]


class ShoperWebhookOrderCreate(BaseModel):
    order_id: Optional[str]
    user_id: Optional[str]
    date: Optional[str]
    status_date: Optional[str]
    confirm_date: Optional[str]
    delivery_date: Optional[str]
    status_id: Optional[str]
    sum: Optional[str]
    payment_id: Optional[str]
    user_order: Optional[str]
    shipping_id: Optional[str]
    shipping_cost: Optional[str]
    email: Optional[str]
    delivery_code: Optional[str]
    code: Optional[str]
    confirm: Optional[str]
    notes: Optional[str]
    notes_priv: Optional[str]
    notes_pub: Optional[str]
    currency_id: Optional[str]
    currency_rate: Optional[str]
    paid: Optional[str]
    ip_address: Optional[str]
    discount_client: Optional[str]
    discount_group: Optional[str]
    discount_levels: Optional[str]
    discount_code: Optional[str]
    shipping_vat: Optional[str]
    shipping_vat_value: Optional[str]
    shipping_vat_name: Optional[str]
    code_id: Optional[str]
    lang_id: Optional[str]
    origin: Optional[str]
    parent_order_id: Optional[str]
    registered: Optional[str]
    billingAddress: ShoperBillingAddress
    deliveryAddress: ShoperOrderAddress
    currency_name: Optional[str]
    shipping: ShoperOrderShipping
    status: ShoperOrderStatus
    payment: ShoperOrderPayment
    promo_code: Optional[str]
    products: List[ShoperOrderProduct]
    additional_fields: List[ShoperOrderAdditionalField]
    children: Optional[List]
