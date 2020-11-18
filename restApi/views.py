from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json
from .models import User
import re

class SignUp(View):    

    def contentTypeValid(self, contentType): 
        return contentType == "application/json"

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
        if self.contentTypeValid(request.content_type) and self.allParametersPresent(request.body.decode("utf-8")):
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


class Login(View): 
    def post(self, request): 
        pass
