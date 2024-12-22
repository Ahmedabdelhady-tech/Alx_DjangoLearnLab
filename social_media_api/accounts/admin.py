from django.contrib import admin
from .models import CustomUserManager, CustomerUser

# Register your models here.

# admin.site.register(CustomUserManager)
admin.site.register(CustomerUser)