from django.http import JsonResponse
from rest_framework import serializers, status

from localistico.location import Location, resolve_location, SearchError


class GSearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=20)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)


def index(request):
    gsearch_query = GSearchSerializer(data=request.GET)
    if not gsearch_query.is_valid():
        return JsonResponse(dict(
            message=gsearch_query.errors,
            status=status.HTTP_404_NOT_FOUND,
        ), status=status.HTTP_404_NOT_FOUND)
    query = request.GET['query']
    location_query = None
    if "latitude" in request.GET and "longitude" in request.GET:
        location_query = Location(
            latitude=request.GET['latitude'],
            longitude=request.GET['longitude'])
    try:
        resp = resolve_location(name=query, location=location_query)
    except SearchError as search_error:
        resp = {'error': str(search_error)}
    return JsonResponse(resp)
