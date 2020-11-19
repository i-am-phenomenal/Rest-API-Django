from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.authtoken.models import Token

class Authentication():

    def isExpired(self, token): 
        timeElapsed = timezone.now() - token.created
        leftTime = timedelta(seconds =settings.TOKEN_EXPIRE_AFTER_SECONDS) - timeElapsed
        return leftTime

    def checkIfTokenExpired(self, token):
        return self.isExpired(token)< timedelta(seconds=0)

    def checkIfTokenExists(self, token): 
        tokenObject = Token.objects.get(key=token)
        if tokenObject is None: 
            return False
        else:
            return True

    def renewTokenIfExpired(self, tokenObject): 
        if self.checkIfTokenExpired(tokenObject):
            tempUser = tokenObject.user
            tokenObject.delete()
            token = Token.objects.create(user=tempUser)
            return token
        else: 
            return tokenObject
        