from localisticoapi.celery import app


@app.task
def resolve_location_async(
        *, callback_url,  name, location):
    try:
        resp = resolve_location(name=name, location=location)
    except SearchError as search_error:
        resp = {'error': str(search_error)}
