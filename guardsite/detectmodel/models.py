from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    
    class Meta:
        db_table = 'uploadimage'
