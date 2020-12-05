from ..utils import Utils 
from rest_framework.authtoken.models import Token
from ..models import User

class AdminTopicEventDecorator(): 
    utils = Utils()

    def checkIfUserAdminForGET(self, function): 
        def innerFunction(referenceToCurrentObject, request): 
            #WIP
            # Fix the only() condiiton 
            params = request.headers
            authToken = params["Authorization"].split(" ")[1]
            tokenExistsCondition = lambda token: Token.objects.filter(key=token).exists()
            isUserAdminCondition = lambda userId: User.objects.get(id=userId).only("isAdmin") if (userId is not None) else False
            tokenObject = Token.objects.get(key=authToken) if tokenExistsCondition(authToken) else None
            userId = tokenObject.user_id if (tokenObject is not None ) else None
            response = function(referenceToCurrentObject, request) if isUserAdminCondition(userId) else utils.returnInvalidResponse("User is not an Admin. Hence cant acces the API ", 401)
            return response
        return innerFunction
