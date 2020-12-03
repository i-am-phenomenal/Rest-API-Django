from django.http import HttpResponse
from django.views import View
import json
from .models import User, Event, UserEventRelationship
from .decorators import Decorators

class AdminView(View): 
    
    def checkIfEmailExists(function): 
        def innerFunction(referenceToCurrentObject, request):
            params =  request.body.decode("utf-8")
            params = json.loads()
            print(params["emailId"], '2wwwwwwwwwwwwwwwwwwwwww')
            return function(referenceToCurrentObject, request)

    @checkIfEmailExists
    def post(self, request):
        pass
