import os
import requests
from pydantic import BaseModel
from typing import List, Optional


class ShoperApiClient:

    def __init__(self, shoper_user: str = None, shoper_password: str = None, shoper_base_url: str = None,
                 token: str = None):
        self.shoper_user = shoper_user or os.getenv("SHOPER_USER")
        self.shoper_password = shoper_password or os.getenv("SHOPER_PASSWD")
        self.shoper_base_url = shoper_base_url or os.getenv("SHOPER_BASE_URL")
        self.token = token or os.getenv("SHOPER_TOKEN") or self._get_token()
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


### MODELS ###

class OrderProductsListItem(BaseModel):
    code: str
    delivery_time: str
    delivery_time_hours: str
    discount_perc: str
    file_options: List[str]
    id: str
    loyalty: Optional[str]
    name: str
    option: str
    order_id: str
    pkwiu: str
    price: str
    product_id: str
    quantity: str
    stock_id: str
    tax: str
    type: str
    unit: str
    unit_fp: str
    weight: str


class OrderProducts(BaseModel):
    count: str
    list: List[OrderProductsListItem]
    page: str
    pages: str
