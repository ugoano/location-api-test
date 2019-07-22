import requests

from localisticoapi.celery import app
from localistico.location import (
    Location, resolve_location, SearchError, APIError)


@app.task(bind=True, max_retries=3, default_retry_delay=5)
def resolve_location_async(self, callback_url,  name, location_dict):
    """Task to call gsearch asynchronously."""
    try:
        location_query = Location(**location_dict) if location_dict else None
        resp = resolve_location(name=name, location=location_query)
    except SearchError as search_error:
        resp = {'error': str(search_error)}
    except APIError as api_error:
        self.retry(exc=api_error)
    requests.post(callback_url, json=resp)
