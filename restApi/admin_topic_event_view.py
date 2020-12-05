from rest_framework.views import APIView
from rest_framework import viewsets
from .admin_topic_event_serializer import AdminTopicEventSerializer
from .models import TopicEventRelationship
from django.http import HttpResponse
from rest_framework import authentication, permissions

class AdminTopicEventView(viewsets.ModelViewSet): 
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = AdminTopicEventSerializer
    # permission_classes = [permissions.IsAdminUser]
    queryset = TopicEventRelationship.objects.all()

    # def list(self, request): 
    #     queryset = 

    # def get(self, request): 
    #     return HttpResponse("Ok")

    # @classmethod
    # def get_extra_actions(cls): 
    #     return []