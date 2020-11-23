import re
import json 
from datetime import datetime

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
