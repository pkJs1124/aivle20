from django.urls import path
from .views import new, upload_image,detectborad,detectborad_list


app_name = 'safetydetects'
urlpatterns = [
    path('', new),
    path('upload/',upload_image,name='upload_image'),
    path('detectborad/',detectborad,name='detectborad' ),
    path('detectborad_list/',detectborad_list,name = 'detectborad_list')
    
    
] 