import requests


SERVER_URL = "http://localhost:8000/gsearch"


def test_gsearch_no_query():
    resp = requests.get(SERVER_URL)
    assert resp.status_code == 404


def test_gsearch_valid_query():
    resp = requests.get("{}?{}".format(SERVER_URL, "query=Localistico"))
    assert resp.status_code == 200
    assert resp.json() == {
        'name': "Localistico",
        'place_id': "bc1ae69dbba7e2c983fd02d2f9a44b3ed33a76b1",
        'international_phone_number': "+44 20 3808 1169",
    }

def test_gsearch_invalid_query():
    query = "T" * 21
    resp = requests.get("{}?query={}".format(SERVER_URL, query))
    assert resp.status_code == 404


def test_gsearch_valid_character_query():
    query = "T" * 20
    resp = requests.get("{}?query={}".format(SERVER_URL, query))
    assert resp.status_code == 200
    assert "error" in resp.json()
