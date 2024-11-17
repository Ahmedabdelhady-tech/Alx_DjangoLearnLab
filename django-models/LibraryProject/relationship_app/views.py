# relationship_app/views.py
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from .models import Book
from django.views.generic.detail import DetailView  
from .models import Library


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library  
    template_name = 'relationship_app/library_detail.html'   
    context_object_name = 'library'  
# login view
class CustomLoginView (LoginView):
    template_name = 'relationship/login.html'
#  logout view
class CustomLogoutview(LogoutView):
    template_name = 'relationship/logout.html'

# new register view

class RegisterView (View):
    def get(self, request):
         form = UserCreationForm()
         return render(request, 'relationship/register.html', {'form': form})
    
    def post(self,request):
        form = UserCreationForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'relationship/register.html', {'form': form})
    
    