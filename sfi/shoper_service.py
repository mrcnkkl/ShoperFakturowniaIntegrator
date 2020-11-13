from sfi.fakturownia_client import FakturowniaApiClient, NewInvoiceRequestBodyNoCustomerTaxId, NewInvoiceRequestNoTaxId
from sfi.shoper_client import ShoperApiClient, ShoperWebhookOrderCreate, ShoperOrderProduct
from typing import List, Dict
from sfi.codes import shoper_id_fakturowania_id
import os


class ShoperWebhookCreateOrderService:

    def __init__(self, shoper_wh_order_create: ShoperWebhookOrderCreate,
                 fac: FakturowniaApiClient = None,
                 sac: ShoperApiClient = None):
        self.shoper_wh_order_create = shoper_wh_order_create
        self.fac = fac or FakturowniaApiClient()
        self.sac = sac or ShoperApiClient()

    def get_product_positions(self) -> List[Dict]:
        positions = []
        for product in self.shoper_wh_order_create.products:
            product: ShoperOrderProduct = product
            f_id = shoper_id_fakturowania_id[product.product_id]
            quant = product.quantity
            positions.append({"product_id": f_id, "quantity": quant})
        return positions

    def new_invoice_call_body(self):
        new_inv_body = NewInvoiceRequestBodyNoCustomerTaxId(
            buyer_name=self.shoper_wh_order_create.billingAddress.company or self.shoper_wh_order_create.billingAddress.firstname + self.shoper_wh_order_create.billingAddress.lastname,
            buyer_post_code=self.shoper_wh_order_create.deliveryAddress.postcode,
            buyer_city=self.shoper_wh_order_create.deliveryAddress.city,
            buyer_street=self.shoper_wh_order_create.deliveryAddress.street1 + " " + self.shoper_wh_order_create.deliveryAddress.street2,
            buyer_first_name=self.shoper_wh_order_create.deliveryAddress.firstname,
            buyer_country=self.shoper_wh_order_create.deliveryAddress.country,
            buyer_email=self.shoper_wh_order_create.email,
            buyer_www="",
            buyer_fax="",
            buyer_phone=self.shoper_wh_order_create.deliveryAddress.phone,
            buyer_tax_no=self.shoper_wh_order_create.billingAddress.tax_id or "",
            positions=self.get_product_positions(),
        )
        return NewInvoiceRequestNoTaxId(
            api_token=os.getenv("FAKTUROWNIA_API_TOKEN") or "",
            invoice=new_inv_body
        )

    def handle_request(self):
        self.fac.create_new_invoice(new_invoice=self.new_invoice_call_body())
