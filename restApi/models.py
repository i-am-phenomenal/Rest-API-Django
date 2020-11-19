from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class User(AbstractBaseUser, models.Model):     
    id = models.AutoField(primary_key=True)
    emailId =models.CharField(max_length=30, default="")
    fullName= models.CharField(max_length=30)
    password=models.CharField(max_length=100)
    age = models.IntegerField()
    insertedAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ('password',)
    USERNAME_FIELD = 'id'


class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    topicName =models.CharField(max_length=40, unique=True)
    shortDesc = models.CharField(max_length=40)
    insertedAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)

class UserTopicRelationship(models.Model): 
    id = models.AutoField(primary_key=True)
    userId =models.ForeignKey(User, on_delete=models.CASCADE)
    topicId = models.ForeignKey(Topic, on_delete=models.CASCADE)
    insertedAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)
    class Meta: 
        unique_together= ['userId', 'topicId']

