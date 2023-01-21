from django.db import models
from datetime import datetime


class Room(models.Model):
    name = models.CharField(max_length=1000)

class Message(models.Model):
    room = models.CharField(max_length=1000000)
    user = models.CharField(max_length=1000000)
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)