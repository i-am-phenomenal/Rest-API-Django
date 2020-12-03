from django.http import HttpResponse
from django.views import View
import json
from .models import User, Event, UserEventRelationship
from .decorators import Decorators
from .utils import Utils

class AdminView(View): 
    
    def checkIfEmailExists(function): 
        utils = Utils()
        def innerFunction(referenceToCurrentObject, request):
            params =  request.body.decode("utf-8")
            params = json.loads(params)
            if User.objects.filter(emailId=params["emailId"]).exists():
                return function(referenceToCurrentObject, request)
            else:
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse("User with the given emailId does not exist!")
                    ),
                    status=500
                )
        return innerFunction

    def checkIfValidParams(function):
        utils = Utils()
        def innerFunction(referenceToCurrentObj, request): 
            params = utils.getParamsFromRequest(request)
            if "emailId" in params: 
                return function(referenceToCurrentObj, request)
            else:
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse("Invalid Params")
                    ),
                    status=500
                )
        return innerFunction

    @checkIfValidParams
    @checkIfEmailExists
    def post(self, request):
        utils = Utils()
        params = utils.getParamsFromRequest(request)
        userObject = User.objects.get(emailId=params["emailId"])
        userObject.isAdmin = True
        userObject.save()
        return HttpResponse(
            json.dumps(
                utils.getGoodResponse(
                    "User has been made an admin !"
                )
            ),
            status=200
        )
