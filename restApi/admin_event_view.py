from django.http import HttpResponse
from django.views import View
import json
from .models import User, Event, UserEventRelationship
from .decorators import Decorators

class AdminEventView(View):
    decorators = Decorators()
    @decorators.validateBasicAuthToken
    def post(self, request):
        pass