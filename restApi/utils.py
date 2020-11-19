import re
import json 


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