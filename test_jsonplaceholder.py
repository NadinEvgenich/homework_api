import pytest
import requests
import json
import jsonpath
from conftest import proxy
from jsonschema import validate

base_url = "http://jsonplaceholder.typicode.com/"
path = "posts/1/"


def test_user():
    response = requests.get(url=base_url + path, proxies=proxy, verify=False)
    jsonData = response.json()
    assert response.status_code == 200
    assert jsonData['userId'] == 1
    assert jsonData['id'] == 1


def test_comment():
    res = requests.get(url=base_url + path + "comments", proxies=proxy, verify=False)
    schema = {
        "type": "array",
        "properties": {
            "data": {
                "type": "object",
                "properties": {
                    "postId": {
                        "type": "number"
                    },
                    "id": {
                        "type": "number"
                    },
                    "name": {
                        "type": "string"
                    },
                    "email": {
                        "type": "string"
                    },
                    "body": {
                        "type": "string"
                    }
                }
            }
        }
    }
    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize('postId', [-1, 0, 'a', 1])
@pytest.mark.xfail(strict=False)
def test_comments(postId):
    response = requests.get(url=base_url + "comments", params={'postId': postId}, proxies=proxy, verify=False)
    jsonData = response.json()
    assert response.status_code == 200
    assert jsonData != []


def test_create_delete_user():
    with open("data/user.json", "r") as f:
        inputData = json.load(f)
    response = requests.post(url=base_url + "posts", json=inputData, proxies=proxy, verify=False)
    responseJson = json.loads(response.text)
    assert response.status_code == 201
    assert jsonpath.jsonpath(responseJson, '$.userId')[0] == inputData["userId"]
    response = requests.delete(url=base_url + path, proxies=proxy, verify=False)
    assert response.status_code == 200


@pytest.mark.parametrize('data', [{"title": 123}, {"title": "qwery"}, {"title": "!@##"}])
def test_patch(data):
    res = requests.patch(url=base_url + path, data=data, proxies=proxy, verify=False)
    jsonData = res.json()
    assert res.status_code == 200
    assert jsonData['title'] != []
