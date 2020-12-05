from rest_framework import serializers
from .models import TopicEventRelationship

class AdminTopicEventSerializer(serializers.ModelSerializer): 
    class Meta:
        model = TopicEventRelationship
        fields = ("id", "topic", "event", "insertedAt", "updatedAt")