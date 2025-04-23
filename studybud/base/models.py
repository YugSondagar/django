from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True,default ="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host =  models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) 
    name = models.CharField(max_length=200) 
    description = models.TextField(null=True, blank=True) 
    participants = models.ManyToManyField(User,related_name='participants',blank=True)  #bcoz we already have User model connected we need related_name and we also want to submit the form without having to check it therefore we use blank=True
    updated = models.DateTimeField(auto_now=True) #auto_now --> Updates the field to the current date and time every time the object is saved.
    created = models.DateTimeField(auto_now_add=True)  #auto_now_add --> Sets the field to the current date and time only when the object is first created

    class Meta:
        ordering = ['-updated','-created']  #this is for adding newest item to the top 
    
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  #CASCADE means, "If the user is deleted, delete all their messages too."
    body = models.TextField(blank=True) 
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True) 


    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.body[0:50]
















'''
Besides CASCADE, there are other options for on_delete:

PROTECT: Don’t allow the User to be deleted if they have messages.

SET_NULL: If the User is deleted, set the user field to NULL (empty).

SET_DEFAULT: If the User is deleted, set the user field to a default value.

DO_NOTHING: Do nothing (not recommended unless you handle it manually).
'''