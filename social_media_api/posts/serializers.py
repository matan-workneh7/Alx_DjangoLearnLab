from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    Handles creation, updating, and listing of posts.
    """
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    excerpt = serializers.ReadOnlyField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'created_at', 'updated_at',
            'is_public', 'likes_count', 'comments_count', 'excerpt'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'likes_count', 'comments_count']


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating posts.
    Only includes fields that can be set during creation.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_public']


class PostUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating posts.
    Allows partial updates of post content.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_public']


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    Handles creation, updating, and listing of comments.
    """
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.StringRelatedField(read_only=True)
    parent = serializers.StringRelatedField(read_only=True)
    is_reply = serializers.ReadOnlyField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'post', 'parent', 
            'created_at', 'updated_at', 'is_reply'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating comments.
    Used when creating new comments on posts.
    """
    class Meta:
        model = Comment
        fields = ['content', 'post', 'parent']


class CommentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating comments.
    Allows updating comment content only.
    """
    class Meta:
        model = Comment
        fields = ['content']


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Like model.
    Handles like/unlike operations.
    """
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'created_at']


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Post model.
    Includes comments and likes information.
    """
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    excerpt = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'created_at', 'updated_at',
            'is_public', 'likes_count', 'comments_count', 'excerpt',
            'comments', 'is_liked'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'likes_count', 'comments_count']
    
    def get_is_liked(self, obj):
        """Check if current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Comment model.
    Includes replies and author information.
    """
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.StringRelatedField(read_only=True)
    parent = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    is_reply = serializers.ReadOnlyField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'post', 'parent',
            'created_at', 'updated_at', 'is_reply', 'replies'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_replies(self, obj):
        """Get replies to this comment."""
        replies = obj.replies.filter(is_deleted=False)
        return CommentSerializer(replies, many=True, context=self.context).data
