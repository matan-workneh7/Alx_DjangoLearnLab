from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Post(models.Model):
    """
    Post model for social media platform.
    Includes title, content, author, and timestamps.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    @property
    def excerpt(self):
        """Return a short excerpt of the content."""
        return self.content[:100] + '...' if len(self.content) > 100 else self.content


class Comment(models.Model):
    """
    Comment model for posts.
    References both Post and User with timestamps.
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_absolute_url(self):
        return reverse('comment-detail', kwargs={'pk': self.pk})
    
    @property
    def is_reply(self):
        """Check if this comment is a reply to another comment."""
        return self.parent is not None


class Like(models.Model):
    """
    Like model for posts.
    Tracks which users have liked which posts.
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'
