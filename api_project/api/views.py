from django.shortcuts import render
from rest_framework import generics 
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets, permissions
from rest_framework.viewsets import ModelViewSet


class BookList(generics.ListAPIView):  
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]