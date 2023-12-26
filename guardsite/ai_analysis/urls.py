from django.urls import path
from . import views

urlpatterns=[
    path('analysis/<int:image_id>',views.ai_analysis_view,name='ai_analysis')
]