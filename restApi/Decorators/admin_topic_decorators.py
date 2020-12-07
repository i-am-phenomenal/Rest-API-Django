from ..utils import Utils 
from ..models import Topic

class AdminTopicDecorators():

    def checkIfTopicExists(self, function):
        def innerFunction(referenceToCurrentObj, request, topicId): 
            utils = Utils()
            topicExists = lambda topicId: Topic.objects.filter(id=topicId).exists()
            response = function(referenceToCurrentObj, request, topicId) if topicExists(topicId) else utils.returnInvalidResponse("Topic with the Id {topicId} does not exist !".format(topicId=topicId), 400)
            return response
        return innerFunction
