import os
import requests
import pprint


class ShoperApiClient:

    def __init__(self, api_user: str = None, api_password: str = None, base_url: str = None, token: str = None):
        self.api_user = api_user or os.getenv("SHOPER_USER")
        self.api_password = api_password or os.getenv("SHOPER_PASSWD")
        self.base_url = base_url or os.getenv("SHOPER_BASE_URL")
        self.token = token or os.getenv("SHOPER_TOKEN") or self._get_token()
        self.auth_header = {"Authorization": f"Bearer {self.token}"}
        print(self.auth_header)

    def _get_token(self):
        URL = f"{self.base_url}/auth"
        resp = requests.post(URL, auth=requests.auth.HTTPBasicAuth(self.api_user, self.api_password)).json()
        token = resp['access_token']
        print(f"token: {token}")
        return token

    def get_order_by_id(self, id: str):
        resp: requests.Response = requests.get(f"{self.base_url}/orders/{id}", headers=self.auth_header)
        pprint.pprint(resp.json())
        return resp