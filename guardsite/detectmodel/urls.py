from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'detectmodel'
urlpatterns = [
   path('',views.index, name ='index'),
   path('upload/', views.danger_post,name ='danger_post'),
   #path('<int:pk>/', views.danger_post, name='danger_post'),
   path('<int:danger_pk>/',views.detail, name='detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)