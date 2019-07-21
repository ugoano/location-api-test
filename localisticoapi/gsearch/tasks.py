import requests

from localisticoapi.celery import app
from localistico.location import Location, resolve_location, SearchError


@app.task
def resolve_location_async(
        *, callback_url,  name, location):
    try:
        resp = resolve_location(name=name, location=Location(**location))
    except SearchError as search_error:
        resp = {'error': str(search_error)}
    requests.post(callback_url, json=resp)
