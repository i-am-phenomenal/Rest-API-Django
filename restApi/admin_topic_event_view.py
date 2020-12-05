from rest_framework.views import APIView
from rest_framework import viewsets
from .admin_topic_event_serializer import AdminTopicEventSerializer
from .models import TopicEventRelationship, Topic, Event
from django.http import HttpResponse
from rest_framework import authentication, permissions
import json
from .utils import Utils

class AdminTopicEventView(viewsets.ModelViewSet): 
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = AdminTopicEventSerializer
    # permission_classes = [permissions.IsAdminUser]
    queryset = TopicEventRelationship.objects.all()

    def get_queryset(self): 
        # getTopicByTopicId = lambda topicId: Topic.objects.get(id=topicId)
        # getEventByEventId = lambda eventId: Event.objects.get(id=eventId)
        formatted = []
        for topicEventRelationship in TopicEventRelationship.objects.all(): 
            # topicObject = getTopicByTopicId(topicEventRelationship.topic)
            # eventObject = getEventByEventId(topicEventRelationship.event)
            formatted.append(
                {
                    "eventName": topicEventRelationship.event.eventName,
                    "topicName": topicEventRelationship.topic.topicName
                }
            )
        return formatted

    def list(self, request): 
        utils = Utils()
        queryset = self.get_queryset()
        print(queryset)
        return HttpResponse(
            json.dumps(
                queryset
            )
        )
        # return HttpResponse("Ok")

    # def get(self, request): 
    #     return HttpResponse("Ok")

    # @classmethod
    # def get_extra_actions(cls): 
    #     return []