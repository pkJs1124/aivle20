from django.urls import path
from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/',views.create, name ='create'),
    path('<int:notice_pk>/',views.detail, name='detail'),
    path('<int:notice_pk>/delete/',views.delete, name= 'delete'),
    path('<int:notice_pk>/update/',views.update, name='update'),
    path('<int:notice_pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:notice_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    
    
]