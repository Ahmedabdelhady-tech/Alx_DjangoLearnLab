from django.urls import path
from .views import (
    BookListView, BookDetailView, BookCreateView,
    BookBatchUpdateView, BookBatchDeleteView
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),  # List all books
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Retrieve book by ID
    path('books/create/', BookCreateView.as_view(), name='book-create'),  # Create a new book
    path('books/update/', BookBatchUpdateView.as_view(), name='book-batch-update'),  # Batch update
    path('books/delete/', BookBatchDeleteView.as_view(), name='book-batch-delete'),  # Batch delete
]
