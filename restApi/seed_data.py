from django.http import HttpResponse
from .models import User, Topic, Event, UserEventRelationship, UserTopicRelationship, TopicEventRelationship
from django.contrib.auth.hashers import make_password
from random import randint
from .error_class import CustomException
from datetime import datetime

def getPasswordHash(password): 
    return make_password(password)

def populateEventTable(): 
    for i in range(0, 20): 
        iter = str(i)
        eventObject = Event(
            id = i,
            eventDescription = "Event Description " + iter,
            eventName = "Event Name " + iter,
            eventType = "Event Type " + iter,
            eventDate = datetime.now(),
            eventDuration = "2 hours ",
            eventHost = "Event Host " + iter,
            eventLocation = "Event Location " + iter,
            insertedAt = datetime.now(),
            updatedAt = datetime.now()
        )
        eventObject.save()

def populateUserTable(): 
    for iter in range(0, 20): 
        userObject = User(
            emailId= "Email-" + str(iter),
            fullName="Full Name-" + str(iter),
            password= getPasswordHash("pass"),
            age = iter,
            id=iter
        )
        userObject.save()
    myUserObject = User(
        emailId = "chat29aditya@gmail.com",
        fullName = "Aditya Chaturvedi",
        password = getPasswordHash("pass"),
        age = 200
    )
    myUserObject.save()

def populateTopicsTable(): 
    for iter in range(0, 20): 
        topicObject = Topic(
            topicName = "Topic Name " + str(iter),
            shortDesc = "This is a short desc for Topic Name " + str(iter),
            id=iter
        )
        topicObject.save()

def getEventByEventId(eventId): 
    try: 
        event = Event.objects.get(id=eventId)
        return event
    except Event.DoesNotExist: 
        print(eventId, "EVENT ID -> ")
        exit()

def getUserByUserId(userId): 
    try: 
        userObject = User.objects.get(id=userId)
        return userObject
    except User.DoesNotExist: 
        print(userId, "USER ID")
        exit()

def getTopicByTopicId(topicId): 
    try: 
        topicObject = Topic.objects.get(id=topicId)
        return topicObject
    except Topic.DoesNotExist: 
        print(topicId, "TOPIC ID")
        exit()

def userExists(userId):
    return User.objects.filter(id=userId).exists()

def UserEventRelationshipDoesNotExist(userId, eventId): 
    return not (userExists(userId) and Event.objects.filter(id=eventId).exists())

def populateTopicEventRelationshipsTable(): 
    getTopicById = lambda topicId: Topic.objects.get(id=topicId)
    getEventById = lambda eventId: Event.objects.get(id=eventId)
    topicEventRelationshipExists = lambda topicId, eventId: TopicEventRelationship.objects.filter(topic=topicId, event=eventId).exists()
    for iter in range(0, 20):
        topicId = randint(0, 19)
        eventId = randint(0, 19)
        topicEventRelationship = TopicEventRelationship(
            id = iter,
            topic = getTopicById(topicId),
            event = getEventById(eventId),
        )
        if topicEventRelationshipExists(topicId, eventId): 
            pass
        else:
            topicEventRelationship.save()

def populateUserEventRelationshipsTable(): 
    for iter in range(0, 20): 
        userId = randint(0, 19)
        eventId = randint(0, 19)
        userObject = getUserByUserId(userId)
        eventObject = getEventByEventId(eventId)
        if UserEventRelationshipDoesNotExist(userId, eventId):
            userEventRelationship = UserEventRelationship(
                userId =userObject,
                eventId = eventObject
            )
            userEventRelationship.save()

def userTopicRelationshipDoesNotExist(userId, topicId): 
    return not (userExists(userId) and Topic.objects.filter(id=topicId).exists())

def populateUserTopicRelationship(): 
    for iter in range(0, 20): 
        userId = randint(0, 10)
        topicId =randint(0, 10)
        userObject = getUserByUserId(userId)
        topicObject = getTopicByTopicId(topicId)
        if userTopicRelationshipDoesNotExist(userId, topicId):
            userTopicRelationship = UserTopicRelationship(
                userId= userObject,
                topicId= Topic.objects.get(id=topicId)
            )
            userTopicRelationship.save()
        else:
            pass 

def populateTables(request):
    populateUserTable()
    populateTopicsTable()
    populateUserTopicRelationship()
    populateEventTable()
    populateUserEventRelationshipsTable()
    populateTopicEventRelationshipsTable()
    return HttpResponse("Done")


def deleteAllUserRecords(): 
    User.objects.all().delete()

def deleteAllTopics(): 
    Topic.objects.all().delete()

def deleteAllUserTopicRelationship(): 
    UserTopicRelationship.objects.all().delete()

def deleteAllEvents():
    Event.objects.all().delete()   

def deleteAllUserEventRelationship(): 
    UserEventRelationship.objects.all().delete()

def deleteAllRecordsFromAllTables(request):
    deleteAllUserRecords()
    deleteAllTopics()
    deleteAllUserTopicRelationship()
    deleteAllEvents()
    deleteAllUserEventRelationship()
    return HttpResponse("All records from all tables deleted successfully !")