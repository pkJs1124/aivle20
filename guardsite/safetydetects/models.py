from django.db import models
from django.conf import settings
from django.urls import reverse
class UploadedImage(models.Model):
    image=models.ImageField(upload_to='uploaded_images/')
    
# Create your models here.


class Tag(models.Model):
    content = models.TextField(unique = True)
    
    def __str__(self):
        return self.content



class Detectborad(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='uploaded_images/')
    danger = models.TextField()
    create_at = models.DateTimeField(auto_now_add = True)
    checked = models.TextField()
    area = models.TextField()
    tags = models.ManyToManyField(Tag,blank=True)
    
    

