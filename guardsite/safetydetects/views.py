from django.shortcuts import render,redirect
from .models import UploadedImage
from .forms import ImageUploadForm
from .forms import ImageUploadForm,DetectboradForm
from .models import Detectborad
# Create your views here.
def new(request):
    return request
 
def upload_image(request):
    if request.method=='POST':
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ai_analysis:ai_analysis',image_id=upload_image.id)
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