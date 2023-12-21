from django.urls import path
from . import views
from views import upload_image


app_name = 'guardsite'
urlpatterns = [
    path('', views.new),
    path('upload/',upload_image,name='upload_image') 
    
]