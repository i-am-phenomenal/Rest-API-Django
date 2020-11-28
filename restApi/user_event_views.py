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
        userEventRelationshipExists = UserEventRelationship.objects.filter(userId=userObject, eventId=eventObject).exists()
        if userEventRelationshipExists: 
            return HttpResponse(
                json.dumps(
                    utils.getBadResponse("User Event relationship already exists !")
                ),
                status=200
            )
        else:
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

    def getFormattedDateTime(self, datetime): 
        date = "/".join([str(datetime.year), str(datetime.month), str(datetime.day)])
        time = ":".join([str(datetime.hour), str(datetime.minute), str(datetime.second)])
        return date + " " + time

    def getFormattedEvents(self, eventIds): 
        formatted = [
            {
                "eventDescription": event.eventDescription,
                "eventName": event.eventName,
                "eventType": event.eventType,
                "eventDate": self.getFormattedDateTime(event.eventDate),
                "eventDuration": event.eventDuration,
                "eventHost": event.eventHost,
                "eventLocation": event.eventLocation
            }
            for event in Event.objects.filter(id__in = eventIds)
        ]
        return formatted

    def getEventsForUserByEmailId(self, emailId): 
        userObject = User.objects.get(emailId=emailId)
        eventIds = list(
            UserEventRelationship.objects.filter(userId=userObject).values_list("eventId", flat=True)   
        )
        return self.getFormattedEvents(eventIds)

    def getAllEventsforCurrentUser(self, userId): 
        userId = int(userId)
        userObject = User.objects.get(id=userId)
        eventIds = list(UserEventRelationship.objects.filter(userId=userObject).values_list("eventId", flat=True))
        formattedEvents = self.getFormattedEvents(eventIds)
        return formattedEvents

    def userWithEmailIdExists(self, emailId):
        return User.objects.filter(emailId=emailId).exists()

    def eventExistsByEventId(self, eventId): 
        return Event.objects.filter(id=eventId).exists()

    def eventExistsByEventName(self, eventName): 
        return Event.objects.filter(eventName=eventName).exists()

    def getUsersWhoSubscribedToAnEvent(self, eventId):
        eventObject = self.getEventByEventNameOrId(eventId)
        userIds = list(
            UserEventRelationship.objects.filter(
            eventId=eventObject
        ).values_list("userId", flat=True))
        formatted = [
            {
                "fullName" : user.fullName,
                "emailId" : user.emailId,
                "age": user.age
            }
            for user in User.objects.filter(id__in = userIds)
        ]
        return formatted

    @decorators.validateToken
    @decorators.validateHeaders
    def get(self, request): 
        utils = Utils()
        params =  request.GET.get("params")
        params = json.loads(params)
        paramKeys = list(params.keys())[0]
        value = params[paramKeys]
        if paramKeys == "userId":
            """ Get all events the user is going to attend """
            events = self.getAllEventsforCurrentUser(value)
            return HttpResponse(
                json.dumps(events)
            )
        
        elif paramKeys == "emailId":
            """ Get all events the user is going to attend """
            if self.userWithEmailIdExists(value):
                events = self.getEventsForUserByEmailId(value)
                return HttpResponse(
                    json.dumps(events)
                )
            else: 
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse("User with the given email ID does not exist !")
                    )
                )

        elif paramKeys == "eventId": 
            """ Get all Users who will attend the given event """
            if self.eventExistsByEventId(value):
                users = self.getUsersWhoSubscribedToAnEvent(value)
                return HttpResponse(
                    json.dumps(
                        users
                    )
                )
            else: 
                HttpResponse(
                    json.dumps(
                        utils.getBadResponse("Event with the given ID does not exist !")
                    )
                )

        elif paramKeys == "eventName": 
            """ Get all Users who will attend the given event """
            if self.eventExistsByEventName(value):
                eventObject = Event.objects.get(eventName= value)
                users = self.getUsersWhoSubscribedToAnEvent(value)
                return HttpResponse(
                    json.dumps(
                        users
                    )
                )
            else: 
                HttpResponse(
                    json.dumps(
                        utils.getBadResponse("Event with the given ID does not exist !")
                    )
                )

