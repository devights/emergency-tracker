from api.views.rest_dispatch import RESTDispatch
from django.http import HttpResponse
import json

class EngineSearch(RESTDispatch):
    """
    Returns incidents for a given vehicle, optional paramater to specify count
    """

    def GET(self, request):

        return HttpResponse(json.dumps(['incident']))
