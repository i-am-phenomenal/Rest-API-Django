from rest_framework import viewsets 
from .admin_topic_serializer import AdminTopicSerializer
from .models import Topic

class AdminTopicView(viewsets.ModelViewSet):
    serializer_class = AdminTopicSerializer
    queryset = Topic.objects.all()