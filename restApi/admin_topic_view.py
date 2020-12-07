from rest_framework import viewsets 
from .admin_topic_serializer import AdminTopicSerializer
from .models import Topic
from django.views import View
from .Decorators.admin_topic_decorators import AdminTopicDecorators
from .Decorators.admin_topic_event_decorators import AdminTopicEventDecorator

class AdminTopicView(viewsets.ModelViewSet):
    serializer_class = AdminTopicSerializer
    queryset = Topic.objects.all()

class AdminTopicGETView(View):
    decorators = AdminTopicDecorators()
    adminTopicEventDecorators = AdminTopicEventDecorator()

    @adminTopicEventDecorators.checkIfUserAdmin
    @decorators.checkIfTopicExists
    def get(self, request, topicId):
        utils = Utils()
        topicObject = Topic.objects.get(id=topicId)
        return HttpResponse(
            json.dumps(
                {
                    "topicName": topicObject.topicName,
                    "shortDesc": topicObject.shortDesc,
                    "insertedAt": utils.convertDateTimeToString(topicObject.insertedAt),
                    "updatedAt": utils.convertDateTimeToString(topicObject.updatedAt)
                }
            ),
            content_type="application/json"
        )