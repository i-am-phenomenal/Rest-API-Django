from .utils import Utils
from .authentication import Authentication
from rest_framework.authtoken.models import Token 
import json 
from .error_class import CustomException
from .models import User, Topic

class Decorators():

    def validateHeaders(self, function): 
        def innerFunction(*args, **kwargs): 
            utils = Utils()
            if utils.contentTypeValid(args[1].content_type): 
                return function(*args, **kwargs)
            else:
                raise CustomException("The Content Type is not valid")
        return innerFunction

    def validateIfTopicExists(self, function):
        def innerFunction(*args, **kwargs):
            params = args[1].body.decode("utf-8")
            params = json.loads(params)
            if "topicName" in params:
                if Topic.objects.filter(topicName=params["topicName"].strip()).exists():
                    return function(*args, **kwargs)
                else:
                    raise CustomException("Topic does not exist !")
            else:
                raise CustomException("topicName not present in request")
        return innerFunction

    def validateToken(self, function): 
        def innerFunction(*args, **kwargs): 
            authentication = Authentication()
            allArgs = []
            if "Authorization" in args[1].headers: 
                token = args[1].headers["Authorization"].split(" ")[1]
                if authentication.checkIfTokenExists(token): 
                    tokenObject = Token.objects.get(key=token)
                    if not authentication.checkIfTokenExpired(tokenObject): 
                        resp = function(*args, **kwargs)
                        return resp
                    else: 
                        raise CustomException("Auth Token already expired")
                else: 
                    raise CustomException("Token does not exist !")
            else: 
                raise CustomException("Invalid Headers")
        return innerFunction