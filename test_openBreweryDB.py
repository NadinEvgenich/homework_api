import pytest
import requests
import json
from conftest import proxy
from jsonschema import validate

Url = "https://api.openbrewerydb.org/breweries/"


def test_get_breweries():
    response = requests.get(url=Url, proxies=proxy, verify=False)
    jsonData = response.json()
    assert response.status_code == 200
    assert jsonData[0]['id'] == "banjo-brewing-fayetteville"
    assert jsonData[0]['name'] == "Banjo Brewing"


@pytest.mark.parametrize("by_city", ["oregon_city", "windsor", "san%20jose"])
def test_filter(by_city):
    response = requests.get(url=Url, params={'by_city': by_city}, proxies=proxy, verify=False)
    assert response.status_code == 200


def get_breweries_id():
    with open("data/breweries.json", "r") as f:
        breweriesData = json.load(f)
        breweriesList = []
        for brewery in breweriesData:
            breweriesList.append(brewery['id'])
    for id in breweriesList:
        yield id


breweries_id = get_breweries_id()


@pytest.mark.parametrize("ids", breweries_id)
def test_validation(ids):
    res = requests.get(url=Url + ids, proxies=proxy, verify=False)

    schema = {
        "type": "object",
        "properties": {
            "data": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string"
                    },
                    "name": {
                        "type": "string"
                    },
                    "brewery_type": {
                        "type": "string"
                    },
                    "street": {
                        "type": [
                            "string",
                            "null"
                        ]
                    },
                    "address_2": {
                        "type": "null"
                    },
                    "address_3": {
                        "type": "null"
                    },
                    "city": {
                        "type": "string"
                    },
                    "state": {
                        "type": "string"
                    },
                    "country_province": {
                        "type": "null"
                    },
                    "postal_code": {
                        "type": "string"
                    },
                    "country": {
                        "type": "string"
                    },
                    "longitude": {
                        "type": [
                            "number",
                            "null"
                        ]
                    },
                    "latitude": {
                        "type": [
                            "number",
                            "null"
                        ]
                    },
                    "phone": {
                        "type": [
                            "number",
                            "null"
                        ]
                    },
                    "website_url": {
                        "type": [
                            "string",
                            "null"
                        ]
                    },
                    "updated_at": {
                        "type": "string"
                    },
                    "created_at": {
                        "type": "string"
                    }
                },
                "required": [
                    "id"
                ]
            }
        }
    }
    validate(instance=res.json(), schema=schema)


@pytest.mark.parametrize("query", ["brewing_co", "enterprises", "brewing%20company"])
def test_search(query):
    response = requests.get(url=Url, params={'query': query}, proxies=proxy, verify=False)
    assert response.status_code == 200


def test_autocomplete():
    res = requests.get(url=Url + "autocomplete", params={'query': 'cerveza'}, proxies=proxy, verify=False)
    resJson = res.json()
    assert len(resJson) <= 15
