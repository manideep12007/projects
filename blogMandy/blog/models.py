from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='pics/',blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if not self.image and not self.content:
            raise ValidationError('atleast image or content should needed to post')
        super(Post,self).save(*args,**kwargs)