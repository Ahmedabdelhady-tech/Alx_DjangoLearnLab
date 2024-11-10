### Delete a Book Instance

```python
# Retrieve the book instance to delete
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
# Delete the book instance
book.delete()
# Verify deletion by trying to retrieve all books
books = Book.objects.all()
print(books)
# Expected Output: <QuerySet []>
