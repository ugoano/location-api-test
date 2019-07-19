from django.http import JsonResponse

from localistico.location import Location, resolve_location


def index(request):
    query = request.GET['query']
    location_query = None
    if "latitude" in request.GET and "longitude" in request.GET:
        location_query = Location(request.GET['latitude'], request.GET['longitude'])
    resp = resolve_location(name=query, location=location_query)
    return JsonResponse(resp)
