from django.views import View
from django.http import HttpResponse
from ..utils import Utils
from ..models import Topic, Event, TopicEventRelationship
from ..Decorators.user_topic_event_decorators import UserTopicEventDecorators
from ..Decorators.decorators import Decorators

class UserTopicEventView(View):
    decorators = UserTopicEventDecorators()
    commonDecorators = Decorators()

    @commonDecorators.validateToken
    @decorators.validateParams
    # @decorators.checkIfTopicAndEventExists
    # @decorators.ifUserSubscribedToTopic
    def get(self, request):
        params = request.GET.get("params")
        return HttpResponse("LOKI")
        
        
        
