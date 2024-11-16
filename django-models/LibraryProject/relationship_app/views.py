# relationship_app/views.py
from django.shortcuts import render
from .models import Book
from django.views.generic import DetailView
from .models import Library

def list_books(request):
    books = Book.objects.all()
    
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library  
    template_name = 'relationship_app/library_detail.html'  
    context_object_name = 'library'  
