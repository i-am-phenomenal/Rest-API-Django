from ..utils import Utils
from ..models import Topic, Event, TopicEventRelationship


class UserTopicEventDecorators():

    def validateParams(self, function):
        def innerFunction(referenceToCurrentObj, request):
            utils = Utils()
            params = utils.getParamsFromRequest(request)
            successCondition = "topicId" in params and "eventId" in params
            response = function(referenceToCurrentObj, request) if successCondition else utils.returnInvalidResponse("Invalid Params", 400)
            return response
        return innerFunction

    def checkIfTopicAndEventExists(self, function):
        def innerFunction(referenceToCurrentObj, request):
            utils = Utils()
            params = utils.getParamsFromRequest(request)
            topicId = params["topicId"]
            eventId = params["eventId"]
            checkIfTopicExistsByTopicId = lambda topicId: Topic.objects.filter(id=topicId).exists()
            checkIfEventExistsByEventId = lambda eventId: Event.objects.filter(id=eventId).exists()
            checkIfRelationshipExists = lambda topicId, eventId: TopicEventRelationship.objects.filter(topic=topicId, event=eventId).exists()
            successCondition = (checkIfTopicExistsByTopicId(topicId) and 
                                        checkIfEventExistsByEventId(eventId) and 
                                        (not checkIfRelationshipExists(topicId, eventId)))
            response = function(referenceToCurrentObj, request) if successCondition else utils.returnInvalidResponse("Either Topic does not exist or Event does not exist or a relationship bw topic and event already exists", 400)
            return response
        return innerFunction