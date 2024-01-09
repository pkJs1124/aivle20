from django.urls import path
from .views import danger_post
from django.conf import settings
from django.conf.urls.static import static


app_name = 'detectmodel'
urlpatterns = [
   path('', danger_post),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)