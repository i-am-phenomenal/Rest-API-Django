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


class GetAdminTopicEventView(View):

    adminTopicEventDecorators = AdminTopicEventDecorator()

    @adminTopicEventDecorators.checkIfUserAdmin
    @adminTopicEventDecorators.checkifTopicEventRelationshipExists
    def get(self, request, topicEventRelationshipId): 
        utils = Utils()
        topicEventRelationship = TopicEventRelationship.objects.get(id=topicEventRelationshipId)
        topic = topicEventRelationship.topic
        event = topicEventRelationship.event
        response = {
            "topic": {
                "topicName": topic.topicName,
                "shortDesc": topic.shortDesc
            },
            "event": {
                "eventName": event.eventName,
                "eventDescription": event.eventDescription,
                "eventType": event.eventType,
                "eventDate": utils.convertDateTimeToString(event.eventDate),
                "eventDuration": event.eventDuration,
                "eventHost": event.eventHost,
                "eventLocation": event.eventLocation
            }
        }
        return HttpResponse(
            json.dumps(
                response
            ),
            content_type="application/json"
        )
    

class AdminTopicEventView(viewsets.ModelViewSet): 
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = AdminTopicEventSerializer
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

    @adminTopicEventDecorators.checkIfUserAdmin
    @adminTopicEventDecorators.checkIfDeleteParamsValid
    @adminTopicEventDecorators.checkIfRecordExistsBasedOnParams
    def delete(self, request):
        utils = Utils()
        params = utils.getParamsFromRequest(request)
        deleteByTopicId = lambda topicId: TopicEventRelationship.objects.filter(topic=topicId).all().delete()
        deleteByEventId = lambda eventId: TopicEventRelationship.objects.filter(event=eventId).all().delete()
        deleteByTopicEventRelationshipId = lambda topicEventRelationshipId: TopicEventRelationship.objects.get(id=topicEventRelationshipId).delete()
        deleteByTopicAndEventId = lambda topicId, eventId: TopicEventRelationship.objects.get(topic=topicId, event=eventId).delete()
        paramsLength = len(params)
        if paramsLength == 1:
            if "topicId" in params:
                topicId = params["topicId"]
                deleteByTopicId(topicId)
                return utils.returnValidResponse("Deleted topic event relationships with topic Ids {topicId}".format(topicId=topicId))

            elif "eventId" in params: 
                eventId = params["eventId"]
                deleteByEventId(eventId)
                return utils.returnValidResponse("Deleted topic event relationships with event ids {eventId}".format(eventId=eventId))

            elif "id" in params: 
                topicEventRelationshipId = params["id"]
                deleteByTopicEventRelationshipId(topicEventRelationshipId)
                return utils.returnValidResponse("Deleted Topic Event Relationship with id {topicEventRelationshipId}".format(topicEventRelationshipId=topicEventRelationshipId))

        elif paramsLength == 2: 
            if "topicId" in params and "eventId" in params: 
                topicId = params["topicId"]
                eventId = params["eventId"]
                topicEventRelationshipId(topicId, eventId)
                return utils.returnValidResponse("Deleted Topic Event Relationship with topicId {topicId} and eventId {eventId}".format(topicId=topicId, eventId=eventId))