import re
import json 
from datetime import datetime
from django.http import HttpResponse

class Utils(): 
    def contentTypeValid(self, contentType): 
        return contentType == "application/json"

    def getBadResponse(self, message): 
        return {
            "errorMessage": message 
        }

    def getGoodResponse(self, message): 
        return {
            "response": message
        }

    def getDecodedParams(self, requestBody): 
        params = requestBody.decode("utf-8")
        params = json.loads(params)
        return params

    #Should be of the format  DD-MM-YYYY
    def getFormattedDateTime(self, strDate):
        strDate = strDate + ", 00:00:00"
        now = datetime.now()
        currentDate = now.strptime(strDate, "%d-%m-%Y, %H:%M:%S")
        return currentDate

    def getParamsFromArgs(self, args):
        params = args[1].body.decode("utf-8")
        params = json.loads(params)
        return params

    def getParamsFromRequest(self, request):
        params = request.body.decode("utf-8")
        params = json.loads(params)
        return params

    def getQueryParameters(self, request, queryParamKey):
        params = request.GET.get(queryParamKey)
        params = json.loads(params)
        return params

    def convertDateTimeToString(self, datetime): 
        date = "/".join([str(datetime.year), str(datetime.month), str(datetime.day)])
        time = ":".join([str(datetime.hour), str(datetime.minute), str(datetime.second)])
        return date + " " + time

    def returnInvalidResponse(referenceToCurrentObj, message, statusCode=500): 
        return HttpResponse(
            json.dumps(
                referenceToCurrentObj.getBadResponse(message)
            ), 
            status=statusCode,
            content_type="application/json"
        )

    def returnValidResponse(referenceToCurrentObj, message): 
        return HttpResponse(
            json.dumps(
                referenceToCurrentObj.getGoodResponse(message)
            ),
            content_type="application/json"
        )