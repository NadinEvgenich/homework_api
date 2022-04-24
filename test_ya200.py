import requests
from conftest import proxy


def test_url_status(base_url, status_code):
    response = requests.get(base_url, proxies=proxy, verify=False)
    assert response.status_code == status_code
