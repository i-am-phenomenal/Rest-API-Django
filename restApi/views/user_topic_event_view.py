from django.views import View
from django.http import HttpResponse
from ..utils import Utils
from ..models import Topic, Event, TopicEventRelationship
from ..Decorators.user_topic_event_decorators import UserTopicEventDecorators
from ..Decorators.decorators import Decorators

class UserTopicEventView(View):
    decorators = UserTopicEventDecorators()
    commonDecorators = Decorators()

    def getEventsWithGivenTopicIdForUser(self, userId, topicId): 
        """
        WIP
        [
            Basic idea is to get list of topics from user_topic_relationship table by userId
            Then get a list of records from topic event relationships and return JSON response
        ]

        Args:
            userId (string): Id of User
            topicId (string): Id of Topic
        """
        topicEventRelationshipExists = lambda topicId:  TopicEventRelationship.objects.filter(topic=topicId).exists()
        getTopicEventRelationshipsByTopicId = lambda topicId: list(TopicEventRelationship.objects.get(topic=topicId).all())
        topicEventRelationships = getTopicEventRelationshipsByTopicId(topicId) # WIP

    @commonDecorators.validateToken
    @decorators.validateParams
    @decorators.checkIfTopicAndEventExists
    @decorators.getUserEmailFromAuthToken
    def get(self, request, userObject):
        utils = Utils()
        params = utils.getQueryParameters(request, "params")
        
        if "topicId" in params: 

            subscribedTopics = self.getEventsWithGivenTopicIdForUser(userObject.id, params["topicId"])

        
        
        
