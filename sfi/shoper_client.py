import os
import requests


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
