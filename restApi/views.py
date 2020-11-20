from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json
from .models import User, Topic, UserTopicRelationship
import re
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate
from .utils import Utils
from .error_class import CustomException
from .authentication import Authentication
from .decorators import Decorators

class SignUp(View, Utils):    

    def getBadResponseObject(self, errorMessage): 
        errorResponse = {
        "error": errorMessage
        }
        return errorResponse

    def allParametersPresent(self, params):
        return  ("fullName" in params) and ("email" in params) and ("age" in params) and ("password" in params)

    def validateEmail(self, emailId): 
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        return re.search(regex, emailId)

    def getPasswordHash(self, password):
        return make_password(password)

    def getGoodResponseObject(self, message):
        response = {
            "message": message
        }
        return response

    def getFormattedUserRecords(self, users):
        formattedRecords = []
        for user in users: 
            formattedRecords.append(
                {
                    "fullName": user.fullName,
                    "age": user.age,
                    "emailId": user.emailId,
                    "password": user.password,
                    # "insertedAt": user.insertedAt,
                    # "updatedAt": user.updatedAt
                }
            )
        return formattedRecords


    def post(self, request): 
        utils = Utils()
        if utils.contentTypeValid(request.content_type) and self.allParametersPresent(request.body.decode("utf-8")):
            parameters = request.body.decode("utf-8")
            parameters = json.loads(parameters)
            if self.validateEmail(parameters["email"]): 
                userObject = User(
                    fullName=parameters["fullName"],
                    age =parameters["age"],
                    password = self.getPasswordHash(parameters["password"]),
                    emailId = parameters["email"]
                )
                userObject.save()
                return HttpResponse(json.dumps(self.getGoodResponseObject("User record saved successfully !")), status=200)
        else: 
            return HttpResponse(json.dumps(self.getBadResponseObject("Invalid Content Type or all parameters are not present")))

    def get(self, request):
        if self.contentTypeValid(request.content_type): 
            allObjects = User.objects.all()
            allObjects = self.getFormattedUserRecords(list(allObjects))
            return HttpResponse(json.dumps(allObjects), status=200)


class Login(View, Utils, Authentication): 
    def post(self, request): 
        utils = Utils()
        authentication = Authentication()
        if utils.contentTypeValid(request.content_type): 
            params = request.body.decode("utf-8")
            params = json.loads(params)
            emailId =params["emailId"]
            plainTextPassword = params["password"]
            if emailId is None or plainTextPassword is None: 
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse("One or more parameters missing")
                    ),
                    status=500
                )
            else: 
                user = User.objects.get(emailId = emailId)
                if check_password(plainTextPassword, user.password): 
                    token, _ =Token.objects.get_or_create(user=user)
                    if authentication.checkIfTokenExpired(token):
                        token = authentication.renewTokenIfExpired(token)
                    return HttpResponse(
                        json.dumps(
                            {
                                "token" : token.key,
                                "userEmailId": user.emailId
                            }
                        )
                    )
                else: 
                    return HttpResponse(
                        json.dumps(
                            utils.getBadResponse("Passwords dont match !")
                        ),
                        status=500
                    )




class TopicOfInterest(View, Utils, Authentication, Decorators): 

    decorators = Decorators()

    def getTopicByTopicId(self, topicId):
        return Topic.objects.get(id=topicId)

    def getTopicByTopicName(self, topicName): 
        topicName = topicName.strip()
        return Topic.objects.get(topicName=topicName)

    def post(self, request): 
        utils = Utils()
        auth = Authentication()
        if "Authorization" in request.headers and utils.contentTypeValid(request.content_type): 
            token = request.headers["Authorization"].split(" ")[1]
            if auth.checkIfTokenExists(token): 
                tokenObject = Token.objects.get(key=token)
                if not auth.checkIfTokenExpired(tokenObject):
                    params = request.body.decode("utf-8")
                    params = json.loads(params)
                    topicObject = Topic(
                        topicName=params["topicName"],
                        shortDesc = params["shortDesc"]
                    )
                    topicObject.save()
                    return HttpResponse(
                        json.dumps(
                            utils.getGoodResponse("Topic Added Successfully !")
                        )
                    )
                else:
                    return HttpResponse(
                        json.dumps(
                            utils.getBadResponse("Token Expired")
                        ),
                        status=500
                    )
            else: 
                return HttpResponse(
                        json.dumps(
                            utils.getBadResponse("Invalid Token !")
                        ),
                        status=500
                    )
        else: 
            return HttpResponse(
                json.dumps(
                    utils.getBadResponse("Invalid Headers !")
                ),
                status=500
            )

    @decorators.validateToken
    @decorators.validateHeaders
    @decorators.validateIfTopicExists
    def put(self, request):
        utils = Utils()
        params = request.body.decode("utf-8")
        params = json.loads(params)
        topicName = params["topicName"].strip()
        topicObject = Topic.objects.get(topicName = topicName)
        if "shortDesc" in params: 
            shortDesc = params["shortDesc"].strip()
            topicObject.topicName = topicName
            topicObject.shortDesc = shortDesc
            topicObject.save()
            return HttpResponse(
                json.dumps(
                    utils.getGoodResponse("Topic Updated Successfully !")
                )
            )
        else: 
            topicObject.topicName = topicName
            topicObject.save()
            return HttpResponse(
                json.dumps(
                    utils.getGoodResponse("Topic Updated Successfully !")
                )
            )

    @decorators.validateToken
    @decorators.validateHeaders
    def delete(self, request):
        utils = Utils()
        params = request.body.decode("utf-8")
        params = json.loads(params)
        nameOrId = params["topic_name_or_id"]
        if type(nameOrId) == int: 
            topicObject = self.getTopicByTopicId(nameOrId)
            topicObject.delete()
            return HttpResponse(
                json.dumps(
                    utils.getGoodResponse("Deleted Topic Successfully !")
                )
            )
        else: 
            try: 
                converted = int(nameOrId)
                topicObject = self.getTopicByTopicId(converted)
                topicObject.delete()
            except ValueError: 
                topicObject = self.getTopicByTopicName(nameOrId)
                topicObject.delete()
            finally: 
                return HttpResponse(
                    json.dumps(
                        utils.getGoodResponse("Deleted topic successfully !")
                    ),
                    status=200
                )

    @decorators.validateToken
    @decorators.validateHeaders
    def get(self, request): 
        queryParam = request.GET.get("name_or_id")
        try: 
            converted = int(queryParam)
            topicObject = self.getTopicByTopicId(converted)
            if topicObject is not None:
                response = {
                    "topicName": topicObject.topicName,
                    "shortDesc": topicObject.shortDesc
                }
                return HttpResponse(
                    json.dumps(
                        response
                    ),
                    status=200
                )
            else: 
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse("Topic Does not exist")
                    )
                )
        except ValueError: 
            topicObject = Topic.objects.get(topicName=queryParam.strip())
            if topicObject is not None: 
                response = {
                    "topicName": topicObject.topicName,
                    "shortDesc": topicObject.shortDesc
                }
                return HttpResponse(
                    json.dumps(
                        response
                    ),
                    status=200
                )
            else: 
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse("Topic Does not exist")
                    )
                )

        # if type(queryParam) == int: 
            
        # return HttpResponse("Ok")
        

class UserTopic(View, Utils, Authentication): 

    def getCurrentLoggedInUser(self, token):
        tokenObject = Token.objects.get(key=token)
        return tokenObject.user
    
    def post(self, request): 
        authentication = Authentication()
        utils = Utils()
        topic = TopicOfInterest()
        if "Authorization" in request.headers and utils.contentTypeValid(request.content_type):
            token = request.headers["Authorization"].split(" ")[1]
            if authentication.checkIfTokenExists(token):
                params = utils.getDecodedParams(request.body)
                topic = topic.getTopicByTopicName(params["topicName"])
                if topic is None: 
                    return HttpResponse(
                        json.dumps(
                            utils.getBadResponse("Topic does not exist !")
                        ),
                        status=500
                    )
                currentUser = self.getCurrentLoggedInUser(token)
                userTopicRelationship = UserTopicRelationship(
                    userId = currentUser,
                    topicId = topic
                )
                userTopicRelationship.save()
                return HttpResponse(
                    json.dumps(
                        utils.getGoodResponse("Added topic for the given user !")
                    )
                )
            else: 
                return HttpResponse(
                    json.dumps(
                        utils.getBadResponse("Invalid Token !")
                    ),
                    status=500
                )
        else:
            return HttpResponse(
                json.dumps(
                    utils.getBadResponse("Invalid Headers !")
                ),
                status=500
            )