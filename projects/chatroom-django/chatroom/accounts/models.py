from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager

class RoomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to="profile_pics/",
                default="profile_pics/default.png",blank=True)
    email = models.EmailField(null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    bio = models.TextField(null=True,blank=True,max_length=500)
    GENDER_OPTIONS = [
        ('M','Male'),
        ('F','Female'),
        ('O','Others')
    ]
    gender = models.CharField(max_length=1,
                choices=GENDER_OPTIONS,default='M')
    def __str__(self):
        return self.username