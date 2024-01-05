from django.urls import path
from .views import *

app_name = 'showreport'
urlpatterns = [
    path('display/<str:date>/', display_checklist, name='display_checklist'),
    path('check/', get_openai_results, name='make_checklist'),
    path('reportlist/', checklist_board, name='checklist_board'),
]
