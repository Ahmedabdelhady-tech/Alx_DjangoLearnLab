### Update a Book Instance

```python
# Retrieve the book instance to update
from bookshelf.models import Book

book = Book.objects.get(title="1984")
# Update the title and save the instance
book.title = "Nineteen Eighty-Four"
book.save()
print(book)
# Expected Output: <Book: Nineteen Eighty-Four>
