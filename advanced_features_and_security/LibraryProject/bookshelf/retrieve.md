### Retrieve a Book Instance

```python
# Retrieve the book instance
from bookshelf.models import Book

book = Book.objects.get(title="1984")
print(book)
print(book.author, book.publication_year)
# Expected Output:
# <Book: 1984>
# George Orwell 1949
