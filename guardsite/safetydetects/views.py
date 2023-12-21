from django.shortcuts import render,redirect
from .forms import ImageUploadForm
# Create your views here.
def new(request):
    return request

def upload_image(request):
    if request.method=='POST':
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('guardsite:main_page')
    else:
        form=ImageUploadForm()
    return render(request, 'index.html',{'form':form})