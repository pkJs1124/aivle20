from django.urls import path
from . import views
app_name='ai_analysis'
urlpatterns=[
    path('analysis/<int:image_id>',views.ai_analysis_view,name='analysis_view')
]