from django.urls import path
from .views import RegisterView, CustomAuthToken, ProfileView,UserListView, UnfollowUserView, FollowUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='users-list'),
    path("follow/<int:user_id>/", FollowUserView.as_view(), name='follow-user'),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view(), name='unfollow-user'),
    
]

