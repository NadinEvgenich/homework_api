import pytest
import requests
import json
import jsonpath
from conftest import proxy

base_url1 = "https://dog.ceo/api/breeds/"
base_url2 = "https://dog.ceo/api/breed/"


@pytest.mark.parametrize("path", ["list/all", "image/random"])
def test_request(path):
    response = requests.get(url=base_url1 + path, proxies=proxy, verify=False)
    assert response.status_code == 200
    assert response.json().get("status") == "success"


@pytest.mark.parametrize("path", ["list/all", "image/random"])
def test_method(path):
    response = requests.post(url=base_url1 + path, proxies=proxy, verify=False)
    assert response.status_code == 405
    assert response.json().get("status") == "error"


def get_breeds():
    with open("data/breeds.json", "r") as f:
        dogsData = json.load(f)
        for dogKey in dogsData:
            yield dogKey


breeds = get_breeds()


@pytest.mark.parametrize("data", breeds)
def test_images(data):
    response = requests.get(url=base_url2 + data + "/images", proxies=proxy, verify=False)
    assert response.status_code == 200
    assert response.json().get("status") == "success"


breeds = get_breeds()


@pytest.mark.parametrize("data", breeds)
@pytest.mark.xfail(strict=False)
def test_list(data):
    response = requests.get(url=base_url2 + data + "/list", proxies=proxy, verify=False)
    responseJson = json.loads(response.text)
    assert response.status_code == 200
    assert response.json().get("status") == "success"
    assert jsonpath.jsonpath(responseJson, 'message') != [[]]


breeds = get_breeds()


@pytest.mark.parametrize("data", breeds)
def test_random_images(data):
    response = requests.get(url=base_url2 + data + "/images/random", proxies=proxy, verify=False)
    assert response.status_code == 200
    assert response.json().get("status") == "success"
