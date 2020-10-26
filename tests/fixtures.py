import pytest
from sfi.shoper_client import *


@pytest.fixture
def shoper_client():
    return ShoperApiClient(api_user="api_user", api_password="api_password", base_url="base_url", token="token")
