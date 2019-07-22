import requests

from localisticoapi.celery import app
from localistico.location import Location, resolve_location, SearchError


@app.task(bind=True, retry_backoff=True)
def resolve_location_async(self, callback_url,  name, location_dict):
    try:
        location_query = Location(**location_dict) if location_dict else None
        resp = resolve_location(name=name, location=Location(**location_dict))
    except SearchError as search_error:
        resp = {'error': str(search_error)}
    except APIError as api_error:
        self.retry(exc=api_error, max_retries=3)
    requests.post(callback_url, json=resp)
