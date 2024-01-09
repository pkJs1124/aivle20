from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'detectmodel'
urlpatterns = [
   path('', views.danger_post,name ='danger_post'),
   path('index/',views.index, name ='index'),
   path('<int:danger_pk>/',views.detail, name='detail'),
] 




+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)