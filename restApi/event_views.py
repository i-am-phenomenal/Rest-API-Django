import json 
from .models import User, Event
from .utils import Utils
from django.http import HttpResponse
from .error_class import CustomException
from django.views import View
from .authentication import Authentication
from .Decorators.decorators import Decorators


class EventView(View, Utils, Decorators):
    decorators = Decorators()

    @decorators.validateToken
    @decorators.validateHeaders
    @decorators.validateEventParams
    def post(self, request):
        utils = Utils()
        params =request.body.decode("utf-8")
        params = json.loads(params)
        eventObject = Event(
            eventName= params["eventName"],
            eventDescription = params["eventDescription"],
            eventType = params["eventType"],
            eventDate = utils.getFormattedDateTime(params["eventDate"]),
            eventDuration = params["eventDuration"],
            eventHost = params["eventHost"],
            eventLocation = params["eventLocation"]
        )
        eventObject.save()
        return HttpResponse(
            json.dumps(
                utils.getGoodResponse(
                "Created Event Successfully with name {eventName}".format(eventName=eventObject.eventName)
                )
            )
        )

    def getEventDictFromObject(self, event): 
        return {
            "eventName": event.eventName,
            "eventDescription": event.eventDescription,
            "eventType": event.eventType,
            "eventDuration": event.eventDuration,
            "eventDate": str(event.eventDate),
            "eventHost": event.eventHost,
            "eventLocation": event.eventLocation
        }

    def checkIfRequiredParamsExists(function):
        def innerFunction(*args, **kwargs):
            nameOrId = args[1].GET.get("eventNameOrId")
            if nameOrId is None: 
                return HttpResponse(
                json.dumps(
                    utils.getBadResponse("No or invalid arguments passed !")
                )
            )
            else: 
                return function(*args, **kwargs)
        return innerFunction

    def checkIfEventExists(function):
        utils = Utils()
        def checkForEventByEventId(eventId):
            return Event.objects.filter(id=eventId).exists() 

        def checkForEventByEventName(params): 
            return Event.objects.filter(eventName=params).exists() 

        def innerFunction(*args, **kwargs): 
            params = args[1].GET.get("eventNameOrId")
            if type(params) == str and params.isnumeric():
                if checkForEventByEventId(params): 
                    return function(*args, **kwargs)
                else: 
                    return HttpResponse(
                        json.dumps(
                            utils.getBadResponse("Event  Does not Exist"),
                            status=200
                        )
                    )
            elif type(params) == int: 
                if checkForEventByEventId(params): 
                    return function(*args, **kwargs)
                else: 
                    return HttpResponse(
                        json.dumps(
                            utils.getBadResponse("Event  Does not Exist"),
                            status=200
                        )
                    )
            elif type(params) == str:
                if checkForEventByEventName(params):
                    return function(*args, **kwargs)
                else: 
                    return HttpResponse(
                        json.dumps(
                            utils.getBadResponse("Event  Does not Exist")
                        ),
                        status=200
                    )
            else:
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse("Invalid Args")
                    )
                )
        return innerFunction

    @decorators.validateToken
    @decorators.validateHeaders
    @checkIfRequiredParamsExists
    @checkIfEventExists
    def get(self, request): 
        nameOrId = request.GET.get("eventNameOrId")
        eventDict = None
        try: 
            nameOrId = int(nameOrId)
            event = Event.objects.get(id=nameOrId)
            eventDict = self.getEventDictFromObject(event)
        except ValueError: 
            event = Event.objects.get(eventName=nameOrId)
            eventDict = self.getEventDictFromObject(event)
        return HttpResponse(
            json.dumps(eventDict),
            status=200
        )

    # @decorators.validateToken
    # @decorators.validateHeaders
    # def put(self, request): 
