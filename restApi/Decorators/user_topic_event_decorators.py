from ..utils import Utils
from ..models import Topic, Event, TopicEventRelationship, User
from rest_framework.authtoken.models import Token


class UserTopicEventDecorators():

    def validateParams(self, function):
        def innerFunction(referenceToCurrentObj, request):
            utils = Utils()
            params = utils.getQueryParameters(request, "params")
            successCondition = "topicId" in params or "eventId" in params or "topicName" in params or "eventName" in params
            response = function(referenceToCurrentObj, request) if successCondition else utils.returnInvalidResponse("Invalid Params", 400)
            return response
        return innerFunction

    def checkIfTopicAndEventExists(self, function):
        def innerFunction(referenceToCurrentObj, request):
            utils = Utils()
            params = utils.getQueryParameters(request, "params")
            invalidTopicResponse = utils.returnInvalidResponse("Topic does not exist", 400)
            invalidEventResponse = utils.returnInvalidResponse("Event does not exist", 400)
            if "topicId" in params: 
                checkIfTopicExistsByTopicId = lambda topicId: Topic.objects.filter(id=topicId).exists()
                response = function(referenceToCurrentObj, request) if checkIfTopicExistsByTopicId(params["topicId"]) else invalidTopicResponse
                return response

            elif "eventId" in params: 
                checkIfEventExistsByEventId = lambda eventId: Event.objects.filter(id=eventId).exists()
                response = function(referenceToCurrentObj, request) if checkIfEventExistsByEventId(params["eventId"]) else invalidEventResponse
                return response

            elif "topicName" in params: 
                checkTopicByTopicName = lambda topicName: Topic.objects.filter(topicName=topicName).exists()
                response = function(referenceToCurrentObj, request) if checkTopicByTopicName(params["topicName"].strip()) else invalidTopicResponse
                return response

            elif "eventName" in params: 
                checkEventByEventName = lambda eventName: Event.objects.filter(eventName=eventName).exists()
                response = function(referenceToCurrentObj, request) if checkEventByEventName(params["eventName"].strip()) else invalidEventResponse
                return response
        return innerFunction

    def getUserEmailFromAuthToken(self, function): 
        def innerFunction(referenceToCurrentObj, request): 
            utils = Utils()
            params = request.headers
            authToken = params["Authorization"].split(" ")[1]
            tokenObject = Token.objects.get(key=authToken)
            userObject = User.objects.get(id=tokenObject.user_id)
            return function(referenceToCurrentObj, request, userObject)
        return innerFunction
            