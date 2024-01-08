from django.urls import path
from .views import upload_and_predict


app_name = 'detectmodel'
urlpatterns = [
   path('', upload_and_predict),
   
] 