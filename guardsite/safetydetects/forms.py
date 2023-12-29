
from django import forms
from .models import UploadedImage, Detectborad
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model=UploadedImage
        fields =['image']
        
    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            logger.debug("Uploaded file content type: %s", image.content_type)
            # 파일 확장자 확인
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError("올바른 이미지 파일 형식이 아닙니다. (jpg, jpeg, png, gif 허용)")

            # 파일 타입 확인 (이미지 파일인지 확인)
            if not image.content_type.startswith('image'):
                raise ValidationError("올바른 이미지 파일 형식이 아닙니다.")

        return image


class DetectboradForm(forms.ModelForm):
    
    class Meta:
        model = Detectborad
        fields = '__all__'
