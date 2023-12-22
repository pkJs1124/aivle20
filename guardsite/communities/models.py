from django.db import models
from django.conf import settings
from django.urls import reverse
# Create your models here.

class Notice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TimeField()
    create_at = models.DateTimeField(auto_now=True)
    etc = models.CharField(max_length=20)
    

        
    def __str__(self):
        return self.title
