from django.db import models
from accounts.models import RoomUser

class Hashtag(models.Model):
    name = models.CharField(max_length=200,unique=True,null=True)
    def __str__(self):
        return self.name 

class Room(models.Model):
    host = models.ForeignKey(RoomUser,on_delete=models.SET_NULL,null=True)
    hashtag = models.ForeignKey(Hashtag,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    information = models.TextField(blank=True,null=True)
    participants = models.ManyToManyField(RoomUser,related_name="joined_rooms",
                                          blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated","-created"]
    
    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    user = models.ForeignKey(RoomUser,on_delete=models.CASCADE)
    chat = models.TextField(max_length=500,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated","-created"]
    
    def __str__(self):
        return self.chat[:50] if len(self.chat)>50 else self.chat