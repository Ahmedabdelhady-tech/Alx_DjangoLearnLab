from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404  # Ensure this is imported
from .models import Post, Like
from notifications.models import Notification

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Use permissions.IsAuthenticated

    def post(self, request, pk):
        # Use get_object_or_404 to fetch the post
        post = get_object_or_404(Post, pk=pk)  
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # Create a notification for the post owner
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post,
            )
            return Response({"message": "Post liked"}, status=201)
        return Response({"message": "You already liked this post"}, status=400)

class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Use permissions.IsAuthenticated

    def post(self, request, pk):
        # Use get_object_or_404 to fetch the post
        post = get_object_or_404(Post, pk=pk)  
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({"message": "Post unliked"}, status=200)
        return Response({"message": "You haven't liked this post"}, status=400)
