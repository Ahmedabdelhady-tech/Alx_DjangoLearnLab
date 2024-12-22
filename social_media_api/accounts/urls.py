from django.urls import path,include
from .views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/', include('posts.urls')),
    "unfollow/<int:user_id>/", "follow/<int:user_id>"
]
 