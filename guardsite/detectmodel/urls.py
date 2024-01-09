from django.urls import path
from .views import danger_post


app_name = 'detectmodel'
urlpatterns = [
   path('', danger_post),
] 