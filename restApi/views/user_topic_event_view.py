from django.views import View
from django.http import HttpResponse
from ..utils import Utils
from ..models import Topic, Event, TopicEventRelationship, UserTopicRelationship, UserEventRelationship
from ..Decorators.user_topic_event_decorators import UserTopicEventDecorators
from ..Decorators.decorators import Decorators

class UserTopicEventView(View):
    decorators = UserTopicEventDecorators()
    commonDecorators = Decorators()

    def getEventsByTopicIdAndUserId(self, topicId, userId): 
        getEventIdsByTopicIds = lambda topicId: list(TopicEventRelationship.objects.filter(topic=topicId).all())
        eventIds = [ record.event_id for record in getEventIdsByTopicIds(topicId) ]
        # getEventDetails =
        print(eventIds, "@@@@@@@@@@@@@@@@@@@@")

    def getEventsForUserSubscribedTopics(self, userId): 
        pass
        # getEventIdsByUserId = lambda userId: list(UserEventRelationship.objects.filter(userId=userId).all())
        # userSubscribedToEvents = lambda userId: UserEventRelationship.objects.filter(userId=userId).exists()
        # records = getEventIdsByUserId(userId) if userSubscribedToEvents(userId) else []
        # print(records, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


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
        userTopicRelationshipExists = lambda topicId, userId: UserTopicRelationship.objects.filter(userId=userId, topicId=topicId).exists()
        # print((topicId, userId), "CCCCCCCCCCCCCCCCCCCCCC")
        # print(userTopicRelationshipExists(topicId, userId), "XXXXXXXXXXXXXXXXXXXXXXXXX")

        records = self.getEventsByTopicIdAndUserId(topicId, userId) if userTopicRelationshipExists(topicId, userId) else self.getEventsForUserSubscribedTopics(userId)
        response = records if (records != []) else 
        # topicEventRelationshipExists = lambda topicId:  TopicEventRelationship.objects.filter(topic=topicId).exists()
        # getTopicEventRelationshipsByTopicId = lambda topicId: list(TopicEventRelationship.objects.get(topic=topicId).all())
        # getUserTopicRelationships = lambda topicId, userId: UserTopicRelationship.objects.get(userId=userId, topicId=topicId)

        # topicEventRelationships = getTopicEventRelationshipsByTopicId(topicId) if topicEventRelationshipExists(topicId) else []


    @commonDecorators.validateToken
    @decorators.validateParams
    @decorators.checkIfTopicAndEventExists
    @decorators.getUserEmailFromAuthToken
    def get(self, request, userObject):
        utils = Utils()
        params = utils.getQueryParameters(request, "params")
        
        if "topicId" in params: 
            subscribedTopics = self.getEventsWithGivenTopicIdForUser(userObject.id, params["topicId"])
            response = HttpResponse(json.dumps(subscribedTopics)) if (subscribedTopics != []) else utils.returnInvalidResponse("There are no Topics or Events for the current user !")
            return response

        
        
        
