from django.http import HttpResponse
from django.views import View
import json
from .models import User, Event, UserEventRelationship
from rest_framework.authtoken.models import Token 
from .utils import Utils
from .authentication import Authentication
from .decorators import Decorators
from .userUtils import UserUtils

class UserEventViews(View, UserUtils, Utils):
    decorators = Decorators()

    def getEventByEventNameOrId(self, eventNameOrId):
        if type(eventNameOrId) == int: 
            return Event.objects.get(id=eventNameOrId)
        elif type(eventNameOrId) == str and eventNameOrId.isnumeric():
            return Event.objects.get(id=eventNameOrId)
        elif type(eventNameOrId) == str:
            return Event.objects.get(eventName = eventNameOrId.strip())

    def validateIfParamsValid(function): 
        utils = Utils()
        def innerFunction(selfObject, request):
            params = utils.getParamsFromRequest(request)
            if "user" in params and "event": 
                return function(selfObject, request)
            else:
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse("User or Event not present in args")
                    )
                )
        return innerFunction

    def validateIfUserAndEventPresent(function):
        utils = Utils()
        def userExists(val): 
            #Val can be either emailId or userId
            if type(val) == str and val.isnumeric():
                return User.objects.filter(id=val).exists()
            elif type(val) == str: 
                return User.objects.filter(emailId=val).exists()
            elif type(val) == int: 
                return User.objects.filter(id=val).exists()

        def eventExists(val): 
            if type(val) == str and val.isnumeric(): 
                return Event.objects.filter(id=val).exists()
            elif type(val) == str: 
                return Event.objects.filter(eventName=val).exists()
            elif type(val) == int:
                return Event.objects.filter(id=val).exists()
                
        def innerFunction(selfObject, request):
            params = utils.getParamsFromRequest(request)
            userNameOrId = params["user"]
            eventNameOrId = params["event"]
            if userExists(userNameOrId) and eventExists(eventNameOrId):
                return function(selfObject, request)
            else: 
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse("User Or Event does not exist ")
                    )
                )
        return innerFunction

    @decorators.validateToken
    @decorators.validateHeaders
    @validateIfParamsValid
    @validateIfUserAndEventPresent
    def post(self, request): 
        utils = Utils()
        userUtils = UserUtils()
        params = request.body.decode("utf-8")
        params = json.loads(params)
        userObject = userUtils.getUserByUserNameOrId(params["user"])
        eventObject = self.getEventByEventNameOrId(params["event"])
        try: 
            _ = UserEventRelationship.objects.filter(userId=userObject.id, eventId=eventObject.id).exists()
            return HttpResponse(
                json.dumps(
                    utils.getBadResponse("User Event relationship already exists !")
                ),
                status=200
            )
        except UserEventRelationship.DoesNotExist: 
            userEventRelationship = UserEventRelationship(
                userId=userObject,
                eventId=eventObject
            )
            userEventRelationship.save()
            return HttpResponse(
                json.dumps(
                    utils.getGoodResponse("User Added to event successfully !")
                )
            )
