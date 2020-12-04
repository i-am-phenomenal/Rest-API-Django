from django.http import HttpResponse
from django.views import View
import json
from .models import User, Event, UserEventRelationship
from .decorators import Decorators
from .utils import Utils
from .error_class  import CustomException

class AdminEventView(View):
    decorators = Decorators()

    def deleteAllEvents(self): 
        Event.objects.all().delete()

    def deleteEventByEventId(self, eventId): 
        utils = Utils()
        try: 
            eventObject = Event.objects.get(id=eventId)
            eventObject.delete()
            return HttpResponse(
                json.dumps(
                    utils.getGoodResponse("Deleted event with the given Id")
                )
            )
        except Event.DoesNotExist as e: 
            print("Exception -> ", e)
            return HttpResponse(
                json.dumps(
                    utils.getBadResponse("Event with the given id does not exist !")
                ),
                status=400
            )

    def deleteEventByEventName(self, eventName):
        utils = Utils()
        try: 
            eventObject = Event.objects.get(eventName=eventName)
            eventObject.delete()
            return HttpResponse(
                json.dumps(
                    utils.getGoodResponse("Deleted event with the given name")
                )
            )
        except Event.DoesNotExist as e: 
            print(e)
            return HttpResponse(
                json.dumps(
                    utils.getBadResponse("Event with the given name does not exist !")
                ),
                status=400
            )

    def deleteEventByParams(self, params): 
        if "eventName" in params:
            return self.deleteEventByEventName(params["eventName"])
        elif  "eventId" in params: 
            return self.deleteEventByEventId(params["eventId"])


    def getListOfAllEvents(self): 
        allEvents = Event.objects.all()
        allEvents = [self.getEventDictByEvent(event) for event in allEvents ]
        return allEvents


    def checkIfValidParams(function):
        utils = Utils()
        def ifRequiredEventFieldsPresent(params): 
            return (
                "eventDescription" in params and
                "eventName" in params and
                "eventType" in params and
                "eventDate" in params and 
                "eventDuration" in params and
                "eventLocation" in params and
                "eventHost" in params
            )

        def innerFunction(referenceToCurrentObj, request): 
            params = utils.getParamsFromRequest(request)
            if (
                "emailId" in params and 
                "event" in params and 
                ifRequiredEventFieldsPresent(params["event"])
            ):
                return function(referenceToCurrentObj, request)
            else: 
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse(
                            "Invalid Params !"
                        )
                    ),
                    status=500
                )
        return innerFunction

    def checkIfValidEventDateFormat(function): 
        utils = Utils()
        def convertToIntIfPossible(element):
            converted = 0
            try: 
                converted = int(element)
            except ValueError as e: 
                print(e)
                raise CustomException("Invalid value in eventDate")
            return converted

        def innerFunction(referenceToCurrentObj, request):
            from datetime import datetime
            params = utils.getParamsFromRequest(request)
            eventDate = params["event"]["eventDate"]
            splitted = list(map(convertToIntIfPossible, eventDate.split("-")))
            day, month, year = splitted
            if (
                len(splitted) == 3 and 
                (0 < day <=  31) and    
                (0 < month <= 12 ) and
                (year >= datetime.now().year)
            ):
                return function(referenceToCurrentObj, request)
            else: 
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse(
                            "event Date format is not valid !"
                        )
                    ),
                    status=500
                )
        return innerFunction
            

    @checkIfValidParams
    @checkIfValidEventDateFormat
    @decorators.validateIfUserIsAdmin
    def post(self, request):
        utils = Utils()
        params = utils.getParamsFromRequest(request)
        eventParams = params["event"]
        eventObject = Event(
            eventName= eventParams["eventName"],
            eventDescription= eventParams["eventDescription"],
            eventType= eventParams["eventType"],
            eventDate = utils.getFormattedDateTime(eventParams["eventDate"]),
            eventDuration= eventParams["eventDuration"],
            eventHost = eventParams["eventHost"],
            eventLocation = eventParams["eventLocation"]
        )
        eventObject.save()
        return HttpResponse(
            json.dumps(
                utils.getGoodResponse("Event Created with ID #{eventId}".format(eventId=eventObject.id))
            ),
            status=200
        )

    def getEventDictByEvent(self, event): 
        utils = Utils()
        return   {
            "eventName" : event.eventName,
            "eventDescription": event.eventDescription,
            "eventType": event.eventType,
            "eventDate": utils.convertDateTimeToString(event.eventDate),
            "eventDuration": event.eventDuration,
            "eventHost": event.eventHost,
            "eventLocation": event.eventLocation
        }  

    def getEventByEventName(self, eventName): 
        utils = Utils()
        if Event.objects.filter(eventName=eventName).exists(): 
            event = Event.objects.get(eventName=eventName)
            return HttpResponse(
                json.dumps(self.getEventDictByEvent(event))
            )
        else: 
            return HttpResponse(
                json.dumps(
                    utils.getBadResponse("Event with given event name does not exist !")
                ),
                status=500
            )

    def getEventByEventId(self, eventId): 
        if Event.objects.filter(id=eventId).exists():
            event = Event.objects.get(id=eventId)
            return HttpResponse(
                json.dumps(self.getEventDictByEvent(event))
            )
        else: 
            return HttpResponse(
                json.dumps(
                    utils.getBadResponse("Event with given event name does not exist !")
                ),
                status=500
            )

    def getEventsByParams(self, params):
        if "eventName" in params: 
            return self.getEventByEventName(params["eventName"])
        elif "eventId" in params: 
            return self.getEventByEventId(params["eventId"])
        else:
            return HttpResponse(
                json.dumps(
                    utils.getBadResponse("Invalid params ")
                ),
                status=500
            )

        
    @decorators.validateIfUserIsAdmin
    def get(self, request): 
        params = request.GET.get("params")
        params = json.loads(params)
        if params["event"] == "all": 
            allEvents = self.getListOfAllEvents()
            return HttpResponse(
                json.dumps(
                    allEvents
                ),
                status=200
            )
        else: 
            return self.getEventsByParams(params["event"])

    @decorators.validateIfUserIsAdmin
    def delete(self, request): 
        utils = Utils()
        params = utils.getParamsFromRequest(request)
        if params["event"] == "all": 
            self.deleteAllEvents()
            return HttpResponse(
                json.dumps(
                    utils.getGoodResponse("Deleted all Events succesfully !")
                )
            )
        else: 
            return self.deleteEventByParams(params["event"])
        
