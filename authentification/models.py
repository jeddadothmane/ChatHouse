from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=1000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)