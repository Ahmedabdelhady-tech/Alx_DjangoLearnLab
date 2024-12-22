from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

# User manager model
class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("email is required.")
        if not password:
            raise ValueError("Password is reqired")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)
    
    
    def __str__(self):
        return self.username