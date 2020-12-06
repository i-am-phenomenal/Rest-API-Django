from rest_framework.views import APIView
from rest_framework import viewsets
from .admin_topic_event_serializer import AdminTopicEventSerializer
from .models import TopicEventRelationship, Topic, Event
from django.http import HttpResponse
from rest_framework import authentication, permissions
import json
from .utils import Utils
from django.views import View
from .Decorators.admin_topic_event_decorators import AdminTopicEventDecorator


class GetAdminTopicView(viewsets.ModelViewSet):
    queryset = TopicEventRelationship.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = AdminTopicEventSerializer

    def getAllTopicEvents(self, request, topicId): 
        return HttpResponse("Dummy response") 

    @classmethod
    def get_extra_actions(cls): 
        return [] 


class AdminTopicEventView(viewsets.ModelViewSet): 
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = AdminTopicEventSerializer
    # permission_classes = [permissions.IsAdminUser]
    queryset = TopicEventRelationship.objects.all()
    adminTopicEventDecorators = AdminTopicEventDecorator()

    def get_queryset(self): 
        formatted = []
        for topicEventRelationship in TopicEventRelationship.objects.all(): 
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
        return HttpResponse(
            json.dumps(
                queryset
            ),
            content_type="application/json"
        )

    @adminTopicEventDecorators.checkIfUserAdmin
    @adminTopicEventDecorators.checkIfParamsValid
    @adminTopicEventDecorators.checkIfTopicAndEventDoesNotExist
    def create(self, request): 
        utils = Utils()
        params = utils.getParamsFromRequest(request)
        getTopicByTopicId =  lambda topicId: Topic.objects.get(id=topicId)
        getEventByEventId = lambda eventId: Event.objects.get(id=eventId)
        topicEventRelationship = TopicEventRelationship(
            topic=getTopicByTopicId(params["topic"]),
            event=getEventByEventId(params["event"]),
            id=params["id"]
        )
        topicEventRelationship.save()
        return utils.returnValidResponse("Added Relationship between Topic and Event !")
