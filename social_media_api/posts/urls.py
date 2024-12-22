from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikeView, LikePostView, UnlikePostView
from . import views


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like_post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike_post'),
]


