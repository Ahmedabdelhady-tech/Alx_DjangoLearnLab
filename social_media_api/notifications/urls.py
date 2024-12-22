from django.urls import path
from .views import NotificationListView, LikeView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('posts/<int:pk>/like/', LikeView.as_view(), name='post-like'),
]