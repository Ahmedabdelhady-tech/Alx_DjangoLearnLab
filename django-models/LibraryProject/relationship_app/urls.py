from django.urls import path
from .views import list_books, LibraryDetailView
from.views import CustomLoginView, CustomLogoutview
from.views import RegisterView


urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutview.as_view(),name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
