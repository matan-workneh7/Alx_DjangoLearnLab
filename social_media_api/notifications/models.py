from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Notification(models.Model):
    """
    Notification model for tracking user interactions.
    Includes recipient, actor, verb, target, and timestamp.
    """
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    actor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='actor_notifications'
    )
    verb = models.CharField(max_length=255)  # Describing the action (e.g., 'liked', 'commented', 'followed')
    target_content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['recipient']),
            models.Index(fields=['actor']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['is_read']),
            models.Index(fields=['target_content_type', 'target_object_id']),
        ]
    
    def __str__(self):
        return f'{self.actor.username} {self.verb} {self.target}'
    
    @property
    def description(self):
        """Generate a human-readable description of the notification."""
        if self.target:
            return f'{self.actor.username} {self.verb} your {self.target.__class__.__name__.lower()}'
        return f'{self.actor.username} {self.verb}'
    
    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
        self.save(update_fields=['is_read'])
    
    def mark_as_unread(self):
        """Mark notification as unread."""
        self.is_read = False
        self.save(update_fields=['is_read'])


class NotificationPreference(models.Model):
    """
    User notification preferences.
    Controls which types of notifications users receive.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='notification_preferences'
    )
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    like_notifications = models.BooleanField(default=True)
    comment_notifications = models.BooleanField(default=True)
    follow_notifications = models.BooleanField(default=True)
    mention_notifications = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f'Notification preferences for {self.user.username}'
