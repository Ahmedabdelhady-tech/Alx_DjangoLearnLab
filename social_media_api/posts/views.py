from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Post, Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
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
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({"message": "Post unliked"}, status=200)
        return Response({"message": "You haven't liked this post"}, status=400)
