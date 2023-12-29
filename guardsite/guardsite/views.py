from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def main_page(request):
   if not request.user.is_authenticated:
       return redirect(reverse("accounts:login"))
   else:
       return render(request,"index.html") 