from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth import authenticate

class UserAccountManager(BaseUserManager):
    def create_user(self, id, password=None):
        if not id:
            raise ValueError('Email must be set!')
        user = self.model(id=id, fullName="Aditya Chaturvedi", password=password, age=23, isAdmin=True)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password):
        user = self.create_user(id, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, id):
        # user = authenticate(emailId=emailId)
        user = self.get(id=id)
        print("111111111111111111111", user)
        return user

class User(AbstractBaseUser, models.Model):     
    id = models.AutoField(primary_key=True)
    emailId =models.CharField(max_length=30, default="")
    fullName= models.CharField(max_length=30)
    password=models.CharField(max_length=100)
    age = models.IntegerField()
    insertedAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)
    isAdmin = models.BooleanField(default=False)
    REQUIRED_FIELDS = ('password',)
    USERNAME_FIELD = 'id'

    objects = UserAccountManager()

    def get_short_name(self):
        return self.emailId

    def get_full_name(self):
        return  self.emailId

    def has_perms(self, perm, ob=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def natural_key(self):
        return self.emailId

    @property
    def is_staff(self):
        self.isAdmin

class TopicManager(models.Manager): 
    def topicNames(self): 
        return self.filter(id__lt = 5)

class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    topicName =models.CharField(max_length=40, unique=True)
    shortDesc = models.CharField(max_length=40)
    insertedAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = TopicManager()

class UserTopicRelationship(models.Model): 
    id = models.AutoField(primary_key=True)
    userId =models.ForeignKey(User, on_delete=models.CASCADE)
    topicId = models.ForeignKey(Topic, on_delete=models.CASCADE)
    insertedAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)
    class Meta: 
        unique_together= ['userId', 'topicId']


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    eventDescription = models.CharField(max_length=100, default="")
    eventName = models.CharField(max_length=50, unique=True)
    eventType =models.CharField(max_length=30)
    eventDate = models.DateTimeField(auto_now=True)
    eventDuration = models.CharField(max_length=20)
    eventHost = models.CharField(max_length=30)
    eventLocation = models.CharField(max_length=30)
    insertedAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)

class UserEventRelationship(models.Model):
    id= models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    eventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    insertedAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    class Meta: 
        unique_together = ("userId", "eventId")


class TopicEventRelationship(models.Model):
    id=models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    insertedAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta: 
        unique_together= ("topic", "event")

# class UserAccount(AbstractBaseUser):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=128)
#     last_name = models.CharField(max_length=128)
#     is_active = models.BooleanField(default=True) # default=False when you are going to implement Activation Mail
#     is_admin = models.BooleanField(default=False)

#     objects = UserAccountManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     def get_short_name(self):
#         return self.email

#     def get_full_name(self):
#         return  self.email

#     def has_perms(self, perm, ob=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True

#     def natural_key(self):
#         return self.email

#     @property
#     def is_staff(self):
#         self.is_admin