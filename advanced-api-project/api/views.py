from django_filters import rest_framework  
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend  
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book
from .serializers import BookSerializer
from rest_framework.filters import OrderingFilter  

# ListView: Retrieve all books with filtering, searching, and ordering
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users

    # Set up filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']  # Fields that can be filtered
    search_fields = ['title', 'author']  # Enable search on title and author
    ordering_fields = ['title', 'publication_year']  # Enable ordering by title and publication year
    ordering = ['title']  # Default ordering by title


# DetailView: Retrieve a single book by ID
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Authenticated users only


# CreateView: Add a new book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Authenticated users only


# UpdateView: Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Authenticated users only


# DeleteView: Remove a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Authenticated users only


# Batch Update for Books
class BookBatchUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        data = request.data  # Expecting a list of book objects
        for book_data in data:
            try:
                book = Book.objects.get(id=book_data['id'])
                serializer = BookSerializer(book, data=book_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Book.DoesNotExist:
                return Response({"error": f"Book with ID {book_data['id']} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Books updated successfully."}, status=status.HTTP_200_OK)


# Batch Delete for Books
class BookBatchDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return Response({"error": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        Book.objects.filter(id__in=ids).delete()
        return Response({"message": "Books deleted successfully."}, status=status.HTTP_200_OK)
