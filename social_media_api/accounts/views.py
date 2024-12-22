from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions, generics
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserRegistrationSerializer, LoginSerializer
from rest_framework.decorators import api_view, permission_classes
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from posts.models import Post  
from posts.serializers import PostSerializer  


class RegisterView(generics.GenericAPIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Allows the current user to follow another user.
    """
    current_user = request.user
    try:
        user_to_follow = CustomUser.objects.get(id=user_id)  # Use CustomUser directly
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if user_to_follow == current_user:
        return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
    
    current_user.following.add(user_to_follow)
    return Response({"detail": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Allows the current user to unfollow another user.
    """
    current_user = request.user
    try:
        user_to_unfollow = CustomUser.objects.get(id=user_id)  # Use CustomUser directly
    except CustomUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if user_to_unfollow == current_user:
        return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    current_user.following.remove(user_to_unfollow)
    return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    """
    Returns a feed of posts from users the current user follows.
    """
    current_user = request.user
    followed_users = current_user.following.all()  # Get users the current user follows
    posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')  # Get posts from followed users
    serializer = PostSerializer(posts, many=True)  # Serialize the posts
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_users(request):
    """
    Lists all users for testing and discovery purposes.
    """
    users = CustomUser.objects.all()  # Explicitly use CustomUser.objects.all()
    user_data = [{"id": user.id, "username": user.username} for user in users]
    return Response(user_data, status=status.HTTP_200_OK)