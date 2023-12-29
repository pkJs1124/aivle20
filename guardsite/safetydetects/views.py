from django.shortcuts import render,redirect
from .models import UploadedImage
from .forms import ImageUploadForm
from .forms import ImageUploadForm,DetectboradForm
from .models import Detectborad
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)
# Create your views here.
def new(request):
    return request
 
def upload_image(request):
    if request.method=='POST':
        form = ImageUploadForm(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            uploaded_image=form.save()
            request.session['uploaded_image_id']=uploaded_image.id
            messages.success(request,"Image uploade successfully.")
            return redirect('ai_analysis:analysis_view',image_id=uploaded_image.id)
        else:
            # 폼 유효성 검사 실패 시 로그
            logger.warning("Form is not valid")
            logger.debug("Form errors: %s", form.errors.as_json())
            
    else:
        form=ImageUploadForm()
    return render(request, 'index.html',{'form':form})


def detectborad_list(request):
    detectborads = Detectborad.objects.all()
    context = {
        'detectborads':detectborads
    }
    return render(request,'borad.html',context)

def detectborad(request):
    if request.method == 'POST':
        form = DetectboradForm(request.POST, request.FILES)
        if form.is_valid():
            # 이미지를 모델에 저장
            detectborad = form.save(commit=False)
            
            # AI 모델에 이미지 전달하여 결과 계산
            # image_result = ai_model_process(detectborad.image)
            detectborad.danger = image_result
            
            # 작성자 정보와 결과를 저장
            detectborad.save()
            return redirect('detectborad_list')
    else:
        form = DetectboradForm()
    
    return render(request, 'index.html', {'form': form})