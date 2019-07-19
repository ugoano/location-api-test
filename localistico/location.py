import requests


APIKEY = 'AIzaSyBDHCARiAh9_LTmreNg74pD_wZF4iyQezU'
stub_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?{}'


class APIError(Exception):
    pass


class Location:

    def __init__(self, *, latitude:float, longitude:float):
        self.latitude = latitude
        self.longitude = longitude


def resolve_location(name:str, location:Location=None):
    params = "query={}".format(name)
    if location:
        params += "&location={},{}".format(location.latitude, location.longitude)
    url = stub_url.format(params)
    resp = requests.get(url)
    if resp.status_code >= 200 and resp.status_code < 300:
        rjson = resp.json()
        if rjson['status'] == "OK":
            return {
                'name': rjson['results'][0]['name'],
                'place_id': rjson['results'][0]['id'],
                'international_phone_number': rjson['results'][0],
            }
        else:
            if "error_message" in rjson:
                raise APIError("Error in Google response: {}".format(rjson['error_message']))
            else:
                raise APIError(rjson['status'])
    else:
        raise APIError("HTTP return code {}".format(resp.status_code))
