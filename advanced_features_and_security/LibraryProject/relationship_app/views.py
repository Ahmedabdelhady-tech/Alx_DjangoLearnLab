from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Library, UserProfile, Author
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.views.generic.detail import DetailView

# 1. Function-Based View to List All Books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# 2. Class-Based View to Show Library Details
class LibraryDetailView(DetailView):
    model = Library  
    template_name = 'relationship_app/library_detail.html'   
    context_object_name = 'library'

# 3. Role Checking Functions for Access Control
def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'

# 4. Views for Different User Roles with Role-Based Access Control
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

# 5. User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically assign MEMBER role to the new user
            UserProfile.objects.create(user=user, role=UserProfile.MEMBER)  
            login(request, user)
            return redirect('home')  # Redirect to home after login
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# 6. User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after login
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# 7. User Logout View
def user_logout(request):
    logout(request)
    return redirect('login') 

# 8. Permission-Required Views for Adding, Editing, and Deleting Books

# View to Add a Book (Requires 'can_add_book' Permission)
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    authors = Author.objects.all()  # Get all authors for selection
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        author = Author.objects.get(id=author_id)  # Get the selected author
        Book.objects.create(title=title, author=author)  # Create a new book
        return redirect('book_list')  # Redirect to book list after creation
    return render(request, 'relationship_app/add_book.html', {'authors': authors})

# View to Edit a Book (Requires 'can_change_book' Permission)
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Get the book by primary key
    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_id = request.POST.get('author')
        book.author = Author.objects.get(id=author_id)  # Update the author
        book.save()  # Save the updated book
        return redirect('book_list')  # Redirect to book list after editing
    authors = Author.objects.all()  # Get all authors for selection
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})

# View to Delete a Book (Requires 'can_delete_book' Permission)
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Get the book by primary key
    if request.method == 'POST':
        book.delete()  # Delete the selected book
        return redirect('book_list')  # Redirect to book list after deletion
    return render(request, 'relationship_app/delete_book.html', {'book': book})

# 9. Book List View (Displays All Books)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})
