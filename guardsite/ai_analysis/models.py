from django.db import models
from safetydetects.models import UploadedImage
# Create your models here.



class AIAnalysisResult(models.Model):
    original_image=models.ForeignKey(UploadedImage,on_delete=models.CASCADE)
    processed_image=models.ImageField(upload_to='processed_image/')
    analysis_text=models.TextField()