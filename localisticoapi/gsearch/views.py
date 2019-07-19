from django.http import JsonResponse

from localistico.location import resolve_location


def index(request):
    resp = resolve_location("My Old Dutch")
    return JsonResponse(resp)
