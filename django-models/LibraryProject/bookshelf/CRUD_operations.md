# CRUD Operations for Book Model

## Create Operation
```python
from bookshelf.models import Book

# Create a new book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
# Expected Output: <Book: 1984>

## Retrieve Operation
```python
from bookshelf.models import Book

# Retrieve the book instance
book = Book.objects.get(title="1984")
print(book)
print(book.author, book.publication_year)
# Expected Output:
# <Book: 1984>
# George Orwell 1949

## Update Operation
```python
from bookshelf.models import Book

# Retrieve the book instance to update
book = Book.objects.get(title="1984")
# Update the title and save the instance
book.title = "Nineteen Eighty-Four"
book.save()
print(book)
# Expected Output: <Book: Nineteen Eighty-Four>

## Delete Operation
```python
from bookshelf.models import Book

# Retrieve the book instance to delete
book = Book.objects.get(title="Nineteen Eighty-Four")
# Delete the book instance
book.delete()
# Verify deletion by trying to retrieve all books
books = Book.objects.all()
print(books)
# Expected Output: <QuerySet []>
