from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm

# ListView: Display all blog posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Template for the list of posts
    context_object_name = 'posts'  # The variable to pass to the template
    ordering = ['-published_date']  # Order by the most recent posts

# DetailView: Display a single post by primary key (ID)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Template for post detail
    context_object_name = 'post'

# CreateView: Allows authenticated users to create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm  # Custom form for Post
    template_name = 'blog/post_form.html'
    success_url = '/'  # Redirect to home page after successful creation

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the current user as the author
        return super().form_valid(form)

# UpdateView: Allows the author of the post to update the post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm  # Custom form for Post
    template_name = 'blog/post_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ensure the author is still the current user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# DeleteView: Allows the author to delete the post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'  # Redirect to home page after successful deletion

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
