from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Post, Comment, Tag
from .forms import (
    CustomUserCreationForm, UserUpdateForm, PostForm, 
    CommentForm, TagForm, SearchForm
)


# Authentication Views
class CustomLoginView(LoginView):
    """
    Custom login view with redirect functionality
    """
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    """
    Custom logout view
    """
    def get_success_url(self):
        return reverse_lazy('home')


def register_view(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Django Blog!')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_view(request):
    """
    User profile view showing user info and posts
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Profile update failed. Please correct the errors below.')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'registration/profile.html', {
        'form': form,
        'user': request.user
    })


# Blog Post Views
class PostListView(ListView):
    """
    List view for all blog posts with pagination and search
    """
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-published_date']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class PostDetailView(DetailView):
    """
    Detail view for individual blog posts
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add comment form for authenticated users
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create view for new blog posts
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update view for editing blog posts
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete view for removing blog posts
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Comment Views
class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new comment on a post
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        messages.success(self.request, 'Comment posted successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing comment
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def form_valid(self, form):
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a comment
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Tag Views
def posts_by_tag_view(request, slug):
    """
    Show all posts with a specific tag
    """
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag).order_by('-published_date')
    
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/posts_by_tag.html', {
        'tag': tag,
        'posts': page_obj,
        'is_paginated': page_obj.has_other_pages()
    })


# Search View
def search_view(request):
    """
    Search functionality for posts
    """
    form = SearchForm(request.GET or None)
    posts = []
    
    if form.is_valid():
        query = form.cleaned_data['query']
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-published_date')
    
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/search_results.html', {
        'form': form,
        'posts': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'query': form.cleaned_data.get('query', '')
    })


# Home View (alias for PostListView)
def home_view(request):
    """
    Home page view showing all posts
    """
    view = PostListView.as_view()
    return view(request)
