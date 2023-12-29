from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def main_page(request):
   if not request.user.is_authenticated:
       return redirect(reverse("accounts:login"))
   else:
       image_id=request.session.get('uploaded_image_id')
       if image_id:
           return redirect('ai_analysis:analysis_view',image_id=image_id)
       return render(request,"index.html") 