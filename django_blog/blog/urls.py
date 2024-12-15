from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login

urlpatterns = [
    path('home/', views.home, name='home'),
    path('post/', views.BlogListView.as_view(), name='posts'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    # path('logout/', logout_then_login, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('post/', views.BlogListView.as_view(), name='posts_list'),
    path('post/new/', views.BlogCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', views.BlogDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', views.BlogUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='add_comment'),
    path('post/comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('post/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('post/tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='tag_posts'),
    path('post/search/', views.SearchPostListView.as_view(), name='search_posts')
]