import pytest
from sfi.shoper_client import *


@pytest.fixture
def shoper_client():
    return ShoperApiClient(shoper_user="api_user", shoper_password="api_password", shoper_base_url="base_url", token="token")
