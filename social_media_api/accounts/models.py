from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Includes additional fields for social media functionality.
    """
    bio = models.TextField(max_length=500, blank=True, help_text="Tell us about yourself")
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True,
        help_text="Upload a profile picture"
    )
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='user_following',
        blank=True,
        help_text="Users that follow this user"
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})
    
    @property
    def followers_count(self):
        """Return the number of followers"""
        return self.followers.count()
    
    @property
    def following_count(self):
        """Return the number of users this user follows"""
        return self.user_following.count()
    
    def follow(self, user_to_follow):
        """Follow another user"""
        if user_to_follow != self and user_to_follow not in self.user_following.all():
            self.user_following.add(user_to_follow)
            return True
        return False
    
    def unfollow(self, user_to_unfollow):
        """Unfollow another user"""
        if user_to_unfollow in self.user_following.all():
            self.user_following.remove(user_to_unfollow)
            return True
        return False
    
    def is_following(self, user):
        """Check if this user follows the given user"""
        return user in self.user_following.all()


class UserProfile(models.Model):
    """
    Extended user profile model for additional user information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    website = models.URLField(blank=True, help_text="Personal website or portfolio")
    location = models.CharField(max_length=100, blank=True, help_text="City, Country")
    birth_date = models.DateField(null=True, blank=True, help_text="Date of birth")
    is_verified = models.BooleanField(default=False, help_text="Verified account status")
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
