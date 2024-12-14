from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend  
from .models import Book
from .serializers import BookSerializer


# Filter class for Book model (custom filter)
class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')  # Case-insensitive partial match
    author = filters.CharFilter(lookup_expr='icontains')
    publication_year = filters.NumberFilter()

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


# ListView: Retrieve all books with filtering, searching, and ordering
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users

    # Set up filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter  # Use the custom filter class
    search_fields = ['title', 'author']  # Enable search on title and author
    ordering_fields = ['title', 'publication_year']  # Enable ordering by title and publication year
    ordering = ['title']  # Default ordering by title


# DetailView: Retrieve a single book by ID
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for unauthenticated users


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
        updated_books = []
        for book_data in data:
            try:
                book = Book.objects.get(id=book_data['id'])
                serializer = BookSerializer(book, data=book_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_books.append(book)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Book.DoesNotExist:
                return Response({"error": f"Book with ID {book_data['id']} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)
        
        if updated_books:
            return Response({"message": "Books updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No books were updated."}, status=status.HTTP_400_BAD_REQUEST)


# Batch Delete for Books
class BookBatchDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return Response({"error": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if any books with these IDs exist
        books_to_delete = Book.objects.filter(id__in=ids)
        if not books_to_delete.exists():
            return Response({"error": "No books found with the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        books_to_delete.delete()
        return Response({"message": "Books deleted successfully."}, status=status.HTTP_200_OK)
