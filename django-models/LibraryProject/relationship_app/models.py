from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ADMIN = 'Admin'
    LIBRARIAN = 'Librarian'
    MEMBER = 'Member'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
        (MEMBER, 'Member'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)

    def __str__(self):
        return f'{self.user.username} - {self.role}'

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
