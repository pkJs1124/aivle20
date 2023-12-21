from django.urls import path
from .views import new, upload_image


app_name = 'guardsite'
urlpatterns = [
    path('', new),
    path('upload/',upload_image,name='upload_image') 
    
]