import requests


APIKEY = 'AIzaSyDEy58qwyPvic8sF5vlqOFFNZDgqmlS4Qw'
places_search_stub_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?{}'
places_detail_stub_url = 'https://maps.googleapis.com/maps/api/place/details/json?{}'


class APIError(Exception):
    pass


class Location:

    def __init__(self, *, latitude:float, longitude:float):
        self.latitude = latitude
        self.longitude = longitude


def google_places_search(query, location):
    params = "query={}&key={}".format(query, APIKEY)
    if location:
        params += "&location={},{}".format(location.latitude, location.longitude)
    url = places_search_stub_url.format(params)
    return validate_response(requests.get(url))


def google_places_detail(place_id):
    params = "placeid={}&key={}".format(place_id, APIKEY)
    url = places_detail_stub_url.format(params)
    return validate_response(requests.get(url))


def validate_response(response):
    if response.status_code < 200 or response.status_code >= 300:
        raise APIError("HTTP return code {}".format(response.status_code))
    rjson = response.json()
    if rjson['status'] != "OK":
        error_message = "Error in Google response: {}"
        raise APIError(error_message.format(rjson.get('error_message', rjson['status'])))
    return rjson


def resolve_location(name:str, location:Location=None):
    search_resp = google_places_search(name, location)

    # Assuming the first result is the best
    place_detail_resp = google_places_detail(search_resp['results'][0]['place_id'])

    # Again, assuming the first result is the best
    place_detail = place_detail_resp['results'][0]

    return {
        'name': place_detail['name'],
        'place_id': place_detail['id'],
        'international_phone_number': place_detail['international_phone_number'],
    }
