from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=get_user_model().objects.all())

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=get_user_model().objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']