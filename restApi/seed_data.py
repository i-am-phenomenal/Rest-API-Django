from django.http import HttpResponse
from .models import User, Topic, Event
from django.contrib.auth.hashers import make_password

def getPasswordHash(password): 
    return make_password(password)

def populateUserTable(): 
    for iter in range(0, 20): 
        userObject = User(
            emailId= "Email-" + str(iter),
            fullName="Full Name-" + str(iter),
            password= getPasswordHash("pass")
            age = iter,
        )
        userObject.save()

def populateTopicsTable(): 
    for iter in range(0, 20): 
        topicObject = Topic(
            topicName = "Topic Name " + str(iter),
            shortDesc = "This is a short desc for Topic Name " + str(iter)
        )
        topicObject.save()

def populateUserTopicRelationship(): 
    for iter in range(0, 20): 
        pass

def populateTables(request):
    populateUserTable()
    populateTopicsTable()
    populateUserTopicRelationship()