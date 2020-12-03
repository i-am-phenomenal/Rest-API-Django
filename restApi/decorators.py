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

    def containsAllKeys(self, function): 
        def innerFunction(*args, **kwargs):
            params = args[1].body.decode("utf-8")
            params = json.loads(params)
            if "userId" in params and "topicId" in params:
                return function(*args, **kwargs)
            else: 
                raise CustomException("One or more parameters are missing !")
        return innerFunction

    def checkIfContainsUserId(self, function):
        def innerFunction(*args, **kwargs):
            if args[1].GET.get("userId") is None: 
                 raise CustomException("UserId query param is not present")
            else:
                return function(*args, **kwargs)
        return innerFunction

    # def validateParamsLength(function):
    #     def outerFunction(self, outerDecorator):
    #         def innerFunction(*args, **kwargs):
    #             params = args[1].GET.get("eventIdOrName")
    #             if params is None: 
    #                 raise CustomException("More than one params passed")
    #             else: 
    #                 return function(*args, **kwargs)
                # params = json.loads(params)
                # if len(params) == 1:
                #     return function(*args, **kwargs)
                # else: 
                #     raise CustomException("More than one params passed")
        #     return innerFunction
        # return outerFunction
    
    # WIP; Second order decorator 
    # @validateParamsLength
    def validateIfParamIsValid(self, function):
        def innerFunction(*args, **kwargs):
            params = args[1].body.decode("utf-8")
            params = json.loads(params)
            for key, _ in params.keys():
                if key == "eventIdOrName":
                    return function(*args, **kwargs)
                else:
                    return HttpResponse(
                        json.dumps(
                            {
                                "msg": "Invalid Args passed"
                            }
                        )
                    )
        return innerFunction

    def validateEventParams(self, function):
        def innerFunction(*args, **kwargs):
            params = args[1].body.decode("utf-8")
            params = json.loads(params)
            possibleKeys = [
                "eventDescription",
                "eventName", 
                "eventType",
                "eventDate",
                "eventDuration",
                "eventHost",
                "eventLocation"
            ]
            for key, value in params.items():
                if key not in possibleKeys:
                    raise CustomException("One or more keys are missing !")
                else:
                    pass
            return function(*args, **kwargs)
        return innerFunction

    def validateBasicAuthToken(self, function):
        def innerFunction(referenceToCurrentObj, request): 
            return function(referenceToCurrentObj, request)
        return innerFunction