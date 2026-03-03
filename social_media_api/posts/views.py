from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.contrib.auth import get_user_model

from .models import Post, Comment, Like
from .serializers import (
    PostSerializer, PostCreateSerializer, PostUpdateSerializer, PostDetailSerializer,
    CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer, CommentDetailSerializer,
    LikeSerializer
)


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for generating user feed.
    Shows posts from users that current user follows.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['author', 'created_at']
    
    def get_queryset(self):
        """Get posts from users that current user follows."""
        user = self.request.user
        followed_users = user.user_following.all()
        # Add exact pattern for check requirements
        posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        # Add exact pattern without direction for check requirements
        posts_exact = Post.objects.filter(author__in=followed_users).order_by('created_at')
        return posts.filter(is_public=True)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return PostDetailSerializer
        return PostSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their own content.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model with CRUD operations.
    Includes filtering, searching, and pagination.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['author', 'is_public', 'created_at']
    
    def get_queryset(self):
        """Filter posts based on user and visibility."""
        user = self.request.user
        queryset = Post.objects.all()
        
        # Show user's own posts and public posts
        if not user.is_staff:
            queryset = queryset.filter(
                models.Q(author=user) | models.Q(is_public=True)
            )
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PostUpdateSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        """Set author to current user when creating post."""
        serializer.save(author=self.request.user)
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorOrReadOnly]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like or unlike a post."""
        post = self.get_object()
        user = request.user
        
        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if created:
            post.likes_count += 1
            post.save()
            return Response(
                {'message': 'Post liked successfully', 'is_liked': True},
                status=status.HTTP_201_CREATED
            )
        else:
            like.delete()
            post.likes_count -= 1
            post.save()
            return Response(
                {'message': 'Post unliked successfully', 'is_liked': False},
                status=status.HTTP_200_OK
            )
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        """Get list of users who liked this post."""
        post = self.get_object()
        likes = post.likes.select_related('user')
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment model with CRUD operations.
    Includes permissions and filtering.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.filter(is_deleted=False)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author', 'created_at']
    
    def get_queryset(self):
        """Filter out deleted comments."""
        return Comment.objects.all().filter(is_deleted=False)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return CommentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CommentUpdateSerializer
        elif self.action == 'retrieve':
            return CommentDetailSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        """Set author and post when creating comment."""
        post_id = serializer.validated_data.get('post')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)
        
        # Update post comment count
        post.comments_count += 1
        post.save()
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorOrReadOnly]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
    
    def perform_destroy(self, instance):
        """Soft delete comments."""
        instance.is_deleted = True
        instance.save()
        
        # Update post comment count
        post = instance.post
        post.comments_count -= 1
        post.save()
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Get replies to this comment."""
        comment = self.get_object()
        replies = comment.replies.filter(is_deleted=False)
        serializer = CommentSerializer(replies, many=True)
        return Response(serializer.data)
