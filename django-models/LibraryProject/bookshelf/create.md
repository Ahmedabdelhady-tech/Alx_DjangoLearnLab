# Create Operation

### Description:
This document describes the steps to create a new instance of the `Book` model in the Django database. 

### Command:

To create a new book titled "1984" by George Orwell, published in 1949, use the following command in the Django shell:

```python
from myapp.models import Book

# Create a new Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Check that the book was created
book
