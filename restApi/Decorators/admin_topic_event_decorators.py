from ..utils import Utils 
from rest_framework.authtoken.models import Token
from ..models import User, Topic, Event, TopicEventRelationship

class AdminTopicEventDecorator(): 
    utils = Utils()

    def checkifTopicEventRelationshipExists(self, function): 
        def innerFunction(referenceToCurrentObj, request, topicEventRelationshipId): 
            utils = Utils()
            checkIfRelationshipExists = lambda topicEventRelationshipId: TopicEventRelationship.objects.filter(id=topicEventRelationshipId).exists()
            response = function(referenceToCurrentObj, request, topicEventRelationshipId) if checkIfRelationshipExists(topicEventRelationshipId) else  utils.returnInvalidResponse("Topic Event Relationship does not exist", 400)
            return response
        return innerFunction

    def checkIfUserAdmin(self, function): 
        def innerFunction(*args, **kwargs):
            params = args[1].headers
            authToken = params["Authorization"].split(" ")[1]
            tokenExistsCondition = lambda token: Token.objects.filter(key=token).exists()
            getUserByUserId = lambda userId: User.objects.get(id=userId)
            tokenObject = Token.objects.get(key=authToken) if tokenExistsCondition(authToken) else None
            userId = tokenObject.user_id if (tokenObject is not None) else None
            userObject = getUserByUserId(userId) if (userId is not None)  else None
            response = function(*args, **kwargs) if (userObject is not None and userObject.isAdmin) else utils.returnInvalidResponse("User is not an Admin. Hence cant acces the API ", 401)
            return response
        return innerFunction

    def checkIfParamsValid(self, function):
        utils = Utils()
        def innerFunction(referenceToCurrentObject, request): 
            params = utils.getParamsFromRequest(request)
            successCondition = ("topic" in params) and ("event" in params) and ("id" in params)
            response = function(referenceToCurrentObject, request) if successCondition else utils.returnInvalidResponse("Invalid Params", 400)
            return response
        return innerFunction

    def checkIfTopicAndEventDoesNotExist(self, function):
        utils = Utils()
        def innerFunction(referenceToCurrentObj, request): 
            params = utils.getParamsFromRequest(request)
            checkIfTopicExists = lambda topicId: Topic.objects.filter(id=topicId).exists()
            checkIfEventExists = lambda eventId: Event.objects.filter(id=eventId).exists()
            checkIfTopicEventRelationshipExists = lambda topicId, eventId: TopicEventRelationship.objects.filter(topic=topicId, event=eventId).exists()
            checkIfRelationshipWithIdExists = lambda topicEventRelationshipId:  TopicEventRelationship.objects.filter(id=topicEventRelationshipId).exists()
            successCondition = (checkIfTopicExists(params["topic"])) and (checkIfEventExists(params["event"])) and (not checkIfTopicEventRelationshipExists(params["topic"], params["event"])) and (not checkIfRelationshipWithIdExists(params["id"]))
            response = function(referenceToCurrentObj, request) if successCondition else utils.returnInvalidResponse("Either topic or event does not exist or Topic Or Event relationship already exists !", 400)
            return response
        return innerFunction