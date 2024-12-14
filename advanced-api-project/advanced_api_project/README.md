# Advanced API Project

This project is a Django application tailored for advanced API development with Django REST Framework. It demonstrates the creation of custom serializers handling complex data structures and nested relationships.

## Setup

### Step 1: Install Django and Django REST Framework

Install Django and Django REST Framework using pip:

```bash
pip install django djangorestframework

### Filtering, Searching, and Ordering

#### **Filtering**
- Filter by title: `/api/books/?title=Book Title`
- Filter by author name: `/api/books/?author__name=Author Name`

#### **Searching**
- Search across title and author name: `/api/books/?search=keyword`

#### **Ordering**
- Order by publication year (ascending): `/api/books/?ordering=publication_year`
- Order by publication year (descending): `/api/books/?ordering=-publication_year`

