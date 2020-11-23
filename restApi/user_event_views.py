from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json
from .models import User, Event, UserEventRelationship
import re
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate
from .utils import Utils
from .error_class import CustomException
from .authentication import Authentication
from .decorators import Decorators

class UserEventViews(View, Utils):
    decorators = Decorators()

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
        # userEventRelationship = UserEventRelationship(
        #     userId = 
        # )
        #WIP
        return HttpResponse("Ok")
