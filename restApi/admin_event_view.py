from django.http import HttpResponse
from django.views import View
import json
from .models import User, Event, UserEventRelationship
from .decorators import Decorators
from .utils import Utils
from .error_class  import CustomException

class AdminEventView(View):
    decorators = Decorators()

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