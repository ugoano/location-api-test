from django.http import JsonResponse
from rest_framework import serializers, status

from localistico.location import Location, resolve_location, SearchError
from .tasks import resolve_location_async


class GSearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=20)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)


class AsyncGSearchSerializer(serializers.Serializer):
    callback_url = serializers.CharField()
    query = serializers.CharField(max_length=20)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)


def send_404(errors):
    return JsonResponse(dict(
        message=errors,
        status=status.HTTP_404_NOT_FOUND,
    ), status=status.HTTP_404_NOT_FOUND)


def prepare_location_query(params):
    location_query = None
    if "latitude" in params and "longitude" in params:
        location_query = dict(
            latitude=params['latitude'],
            longitude=params['longitude'])
    return location_query


def sync_index(request):
    gsearch_query = GSearchSerializer(data=request.GET)
    if not gsearch_query.is_valid():
        return send_404(gsearch_query.errors)

    query = request.GET['query']
    location_dict = prepare_location_query(request.GET)
    location_query = Location(**location_dict) if location_dict else None

    try:
        resp = resolve_location(name=query, location=location_query)
    except SearchError as search_error:
        resp = {'error': str(search_error)}
    return JsonResponse(resp)


def async_index(request):
    gsearch_query = AsyncGSearchSerializer(data=request.GET)
    if not gsearch_query.is_valid():
        return send_404(gsearch_query.errors)

    query = request.GET['query']
    callback_url = request.GET['callback_url']
    location_dict = prepare_location_query(request.GET)

    try:
        search_task = resolve_location_async.delay(
            callback_url=callback_url, name=query,
            location=location_dict)
        response = {'task_id': search_task.id}
    except Exception as task_error:
        response = {'error': str(task_error)}
    return JsonResponse(response)
