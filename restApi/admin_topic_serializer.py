from rest_framework import serializers
from .models import Topic

class AdminTopicSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Topic
        fields = ("id", "topicName", "shortDesc", "insertedAt", "updatedAt")