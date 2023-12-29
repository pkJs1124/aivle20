from django.shortcuts import render
from safetydetects.models import UploadedImage
from .models import AIAnalysisResult
from .ai_model import apply_object_detection
from django.views.decorators.http import require_POST
# Create your views here.

#@require_POST
def ai_analysis_view(request,image_id):
    
    original_image=UploadedImage.objects.get(id=image_id)
    processed_image_path, analsis_text=apply_object_detection(original_image.image.path)
    analysis_result = AIAnalysisResult.objects.create(
        original_image=original_image,
        processed_image=processed_image_path,
        analysis_text=analsis_text
    )
    return render(request,'ai_anlaysis/ai_analysis.html',{'result':analysis_result})
