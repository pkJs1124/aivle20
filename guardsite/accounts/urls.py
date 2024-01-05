from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('loading/', views.loading_view, name='loading'),
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("toscheck/", views.toscheck, name='toscheck'),
    path("toscheck/signup/", views.signup, name='signup'),
    path("find/", views.find, name='find'),
    path("findpassword/", views.findpassword, name='findpassword'),
    path("findpassword/reset_password", views.resetpassword, name='resetpassword'),
]