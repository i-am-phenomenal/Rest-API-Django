from rest_framework.views import APIView
from rest_framework import viewsets
from .admin_topic_event_serializer import AdminTopicEventSerializer
from .models import TopicEventRelationship, Topic, Event
from django.http import HttpResponse
from rest_framework import authentication, permissions
import json
from .utils import Utils
from .Decorators.admin_topic_event_decorators import AdminTopicEventDecorator

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
            )
        )

    @adminTopicEventDecorators.checkIfUserAdmin
    @adminTopicEventDecorators.checkIfParamsValid
    @adminTopicEventDecorators.checkIfTopicAndEventDoesNotExist
    def create(self, request): 
        utils = Utils()
        params = utils.getParamsFromRequest(request)
        # getTopicByTopicId =  lambda topicId: Topic.objects.
        # topicEventRelationship = TopicEventRelationship(
        #     topi
        # )
        return utils.returnValidResponse("aslkdawndlwedk;lkj")

    def retreive(self, request): 
        utils = Utils()
        return utils.returnValidResponse("Okkkkk")