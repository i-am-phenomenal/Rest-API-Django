from django.http import HttpResponse
from django.views import View
import json
from .models import User, Event, UserEventRelationship
from rest_framework.authtoken.models import Token 
from .utils import Utils
from .authentication import Authentication
from .decorators import Decorators

class UserUtils(Utils):

    def getUserByUserNameOrId(self, userNameOrId):
        if type(userNameOrId) == int: 
            return User.objects.get(id=userNameOrId)
        elif type(userNameOrId) == str and userNameOrId.isnumeric():
            userId = int(userNameOrId)
            return User.objects.get(id=userId)
        elif type(userNameOrId) == str: 
            return User.objects.get(emailId=userNameOrId.strip())

