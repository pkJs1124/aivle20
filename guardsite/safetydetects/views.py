from django.shortcuts import render,redirect
from .models import UploadedImage
from .forms import ImageUploadForm
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