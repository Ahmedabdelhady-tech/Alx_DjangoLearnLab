from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import Author, Book


class BookAPITests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a token for the user
        self.token = Token.objects.create(user=self.user)

        # Set token in the headers for authenticated requests
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # self.client.login

        # Create an author and a book for testing
        self.author = Author.objects.create(name='George Orwell')
        self.book = Book.objects.create(
            title='1984',
            author=self.author,
            publication_year=1949
        )

    def test_create_book(self):
        url = reverse('create-books')  # Your Book Create URL
        data = {
            'title': 'Animal Farm',
            'author': self.author.id,
            'publication_year': 1945
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=2).title, 'Animal Farm')

    def test_get_books(self):
        url = reverse('book-list')  # Your Book List URL
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_book(self):
        url = reverse('update-books', args=[self.book.pk])  # Your Book Update URL
        data = {'title': '1985', 'author': self.author.id, 'publication_year': 1949}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, '1985')

    def test_delete_book(self):
        url = reverse('delete-books', args=[self.book.pk])  # Your Book Delete URL
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_permission_denied_for_unauthenticated_user(self):
        self.client.logout()
        url = reverse('create-books')
        data = {
            'title': 'Unauthorized Book',
            'author': self.author.id,
            'publication_year': 2022
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_books_by_author(self):
        url = f"/api/books/?author={self.author.id}"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author.id)

    def test_search_books(self):
        url = "/api/books/?search=1984"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_order_books_by_title(self):
        url = "/api/books/?ordering=title"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the books are ordered by title