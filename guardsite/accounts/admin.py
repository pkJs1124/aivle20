from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User

# Register your models here.
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     pass

admin.site.register(User)