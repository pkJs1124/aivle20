from django.urls import path
from .views import *

urlpatterns = [
    path('display/', display_checklist, name='display_images'),
]